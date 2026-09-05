"""The 3-evaluation grass rule as a derivative-free line search, plus
the classical inner loops it is benchmarked against (golden section,
Brent), sharing one outer loop: iterated line search on [0,1]^d.

The grass inner is a faithful port of the paper's exact machinery
(papers/grass/numerics2.py): zeta for exterior/stay values, the
three-shot optimal bracket rho*(b) from Table 1, and the stationarity
quartic x^4 - (b - rho d) x^3 + rho (d - rho b) x - rho^2 = 0 for the
interior optimum. Two things the paper takes as given are estimated
online from the run's own evaluations, since an optimizer has no
oracle for them: the standardization (running mean/std of observed
values, negated so minimizing f is maximizing X) and the OU
mean-reversion rate kappa (least-squares fit of the variogram
2(1 - e^{-kappa D}) over recent same-line pairs).

Adaptations forced by the optimization context, all listed here:
  - values are standardized with the mean/std snapshot taken at line
    start; the paper's b is the anchor's standardized value;
  - placements are clipped to the feasible alpha segment of the cube;
  - "flee" (independence, rho -> 0) means the far end of the segment;
  - a "stay" verdict on the third shot spends no evaluation -- the
    line ends after one probe, which is the rule's built-in economy;
  - for b beyond the table (b > 1.2) rho*(b) is extrapolated linearly
    from the last two rows and clipped at 0.95.
"""

import numpy as np
from scipy.special import erf as _erf
from scipy.special import ndtri as _ndtri

# ---------------------------------------------------------------------------
# Exact policy pieces (ported from papers/grass/numerics2.py)
# ---------------------------------------------------------------------------


def zeta(y):
    """Two-shot log-value of an anchor at standardized value y."""
    return 0.5 if y < 0 else ((y * y + 1) / 2 if y <= 1 else float(y))


def interior_optimum(b, d, rho):
    """Best interior placement on a bracket with anchor values (b, d)
    and correlation rho: returns (log_value, x_root) with x_root the
    correlation lambda_2 of the optimum to the b-anchor, or
    (-inf, None) when no real quartic root lies in (rho, 1)."""
    coeffs = [1.0, -(b - rho * d), 0.0, rho * (d - rho * b), -(rho**2)]
    best, best_x = -np.inf, None
    for r in np.roots(coeffs):
        if abs(r.imag) < 1e-9 and rho < r.real < 1:
            x = r.real
            lam = rho / x
            den = 1 - rho * rho
            mu = (x * (1 - lam**2) * b + lam * (1 - x**2) * d) / den
            nu = (1 - x**2) * (1 - lam**2) / den
            val = mu + nu / 2
            if val > best:
                best, best_x = val, x
    return best, best_x


# Three-shot optimal bracket correlation rho*(b), Table 1 of the paper
# (adaptive quadrature, interior allowed). b <= 0 is flee (rho* -> 0).
_RHO_TABLE_B = np.array([0.0, 0.1, 0.3, 0.5, 0.7, 0.83, 0.9, 1.2])
_RHO_TABLE_R = np.array([0.0, 0.053, 0.167, 0.289, 0.402, 0.469, 0.502, 0.622])


def rho_star(b):
    """Interpolated three-shot bracket correlation for anchor value b."""
    if b <= 0.0:
        return 0.0
    if b >= 1.2:
        slope = (0.622 - 0.502) / 0.3
        return min(0.95, 0.622 + slope * (b - 1.2))
    return float(np.interp(b, _RHO_TABLE_B, _RHO_TABLE_R))


# ---------------------------------------------------------------------------
# Budgeted evaluation
# ---------------------------------------------------------------------------


class Budget:
    """Wraps the objective with a global evaluation budget and best-so-far
    tracking. All inner searches draw from the same budget."""

    def __init__(self, objective, n_trials):
        self.objective = objective
        self.n_trials = n_trials
        self.evaluations = 0
        self.best_value = np.inf
        self.best_x = None

    def remaining(self):
        return self.n_trials - self.evaluations

    def __call__(self, x):
        x = np.clip(np.asarray(x, dtype=float), 0.0, 1.0)
        self.evaluations += 1
        v = float(self.objective(list(x)))
        if v < self.best_value:
            self.best_value = v
            self.best_x = x.copy()
        return v


def alpha_range(p, v):
    """Feasible [lo, hi] (containing 0) with p + alpha v in [0,1]^d."""
    lo, hi = -np.inf, np.inf
    for pi, vi in zip(p, v):
        if abs(vi) <= 1e-12:
            continue
        b1, b2 = -pi / vi, (1.0 - pi) / vi
        a, b = (b1, b2) if b1 < b2 else (b2, b1)
        lo, hi = max(lo, a), min(hi, b)
    if not np.isfinite(lo) or not np.isfinite(hi):
        return 0.0, 0.0
    return lo, hi


# ---------------------------------------------------------------------------
# Inner line searches. Each takes (budget, p, fp, v, rng) and returns the
# best (x, f) found on the line (p itself allowed), drawing global budget.
# ---------------------------------------------------------------------------


def golden_inner(k):
    """Golden-section on the feasible segment with at most k evaluations
    (k >= 2): two initial interior probes, then k-2 shrink steps."""
    invphi = (np.sqrt(5.0) - 1) / 2

    def search(budget, p, fp, v, rng):
        lo, hi = alpha_range(p, v)
        if hi - lo < 1e-9:
            return p, fp
        best_a, best_f = 0.0, fp

        def ev(t):
            nonlocal best_a, best_f
            f = budget(p + t * v)
            if f < best_f:
                best_a, best_f = t, f
            return f

        a, b = lo, hi
        c = b - invphi * (b - a)
        d = a + invphi * (b - a)
        if budget.remaining() <= 0:
            return p, fp
        fc = ev(c)
        if budget.remaining() <= 0:
            return np.clip(p + best_a * v, 0, 1), best_f
        fd = ev(d)
        for _ in range(k - 2):
            if budget.remaining() <= 0:
                break
            if fc < fd:
                b, d, fd = d, c, fc
                c = b - invphi * (b - a)
                fc = ev(c)
            else:
                a, c, fc = c, d, fd
                d = a + invphi * (b - a)
                fd = ev(d)
        return np.clip(p + best_a * v, 0, 1), best_f

    return search


def brent_inner(max_evals=10):
    """Downhill bracket + Brent on the feasible segment, ported from
    humpday's Powell._linesearch_powell (scipy's Brent adaptation),
    with a per-line evaluation cap."""

    def search(budget, p, fp, v, rng):
        lo, hi = alpha_range(p, v)
        if hi - lo < 1e-9:
            return p, fp
        state = {"n": 0, "best_a": 0.0, "best_f": fp}

        def ev(t):
            if state["n"] >= max_evals or budget.remaining() <= 0:
                return None
            state["n"] += 1
            f = budget(p + t * v)
            if f < state["best_f"]:
                state["best_a"], state["best_f"] = t, f
            return f

        def done():
            return np.clip(p + state["best_a"] * v, 0, 1), state["best_f"]

        span = hi - lo
        xa = 0.0 if lo < 0 < hi else lo
        xb = xa + min(span * 0.1, 1e-1)
        if xb >= hi:
            xb = lo + 0.5 * span
        fa, fb = ev(xa), ev(xb)
        if fa is None or fb is None:
            return done()
        if fa < fb:
            xa, xb, fa, fb = xb, xa, fb, fa
        gold = 1.618033988749895
        xc = float(np.clip(xb + gold * (xb - xa), lo, hi))
        fc = ev(xc)
        if fc is None:
            return done()
        for _ in range(20):
            if fc >= fb:
                break
            new_xc = xc + gold * (xc - xb)
            if new_xc > hi or new_xc < lo:
                new_xc = hi if (xc - xb) > 0 else lo
                if new_xc == xc:
                    break
            xa, xb, fa, fb = xb, xc, fb, fc
            xc = new_xc
            fc = ev(xc)
            if fc is None:
                return done()
        if not ((xa < xb < xc) or (xc < xb < xa)) or not (fb <= fa and fb <= fc):
            return done()
        a_, b_ = (xc, xa) if xa > xc else (xa, xc)
        x = w = wv = xb
        fx = fw = fv = fb
        deltax = rat = 0.0
        cg = 0.3819660
        for _ in range(50):
            tol1 = 1.48e-3 * abs(x) + 1e-11
            tol2 = 2 * tol1
            xmid = 0.5 * (a_ + b_)
            if abs(x - xmid) < (tol2 - 0.5 * (b_ - a_)):
                break
            if abs(deltax) <= tol1:
                deltax = (a_ - x) if x >= xmid else (b_ - x)
                rat = cg * deltax
            else:
                tmp1 = (x - w) * (fx - fv)
                tmp2 = (x - wv) * (fx - fw)
                p_ = (x - wv) * tmp2 - (x - w) * tmp1
                tmp2 = 2 * (tmp2 - tmp1)
                if tmp2 > 0:
                    p_ = -p_
                tmp2 = abs(tmp2)
                dx_temp = deltax
                deltax = rat
                if (
                    p_ > tmp2 * (a_ - x)
                    and p_ < tmp2 * (b_ - x)
                    and abs(p_) < abs(0.5 * tmp2 * dx_temp)
                ):
                    rat = p_ / tmp2
                    u = x + rat
                    if (u - a_) < tol2 or (b_ - u) < tol2:
                        rat = tol1 if (xmid - x) >= 0 else -tol1
                else:
                    deltax = (a_ - x) if x >= xmid else (b_ - x)
                    rat = cg * deltax
            u = x + (tol1 if rat >= 0 else -tol1) if abs(rat) < tol1 else x + rat
            fu = ev(u)
            if fu is None:
                break
            if fu > fx:
                if u < x:
                    a_ = u
                else:
                    b_ = u
                if fu <= fw or w == x:
                    wv, fv, w, fw = w, fw, u, fu
                elif fu <= fv or wv == x or wv == w:
                    wv, fv = u, fu
            else:
                if u >= x:
                    a_ = x
                else:
                    b_ = x
                wv, fv, w, fw = w, fw, x, fx
                x, fx = u, fu
        return done()

    return search


class GrassInner:
    """The 3-shot OU terminal-placement rule as a line search.

    Carries run-level state: the value history for standardization and
    the same-line pair history for the kappa fit."""

    KAPPA_GRID = np.geomspace(2.0, 200.0, 60)
    CHI2_MEDIAN = 0.4549364  # median of chi^2_1: med[(dX)^2] = 2(1-rho)*this

    def __init__(
        self,
        kappa0=20.0,
        skip_third=False,
        adapt_kappa=True,
        uniform_flee=False,
        placement="table",
        ei_margin=1.05,
        standardize="linear",
    ):
        self.kappa = kappa0
        self.values = []  # all raw values seen (for mean/std)
        self.pairs = []  # (distance, f_i, f_j) raw same-line pairs
        self.stall = 0  # consecutive lines with no material improvement
        # Ablation switches (exp2c mechanism study):
        self.skip_third = skip_third  # two-shot rule only: 1 eval/line
        self.adapt_kappa = adapt_kappa  # False freezes kappa at kappa0
        self.uniform_flee = uniform_flee  # flee to a uniform point on the
        # far half of the segment instead of its end (removes the
        # cube-boundary bias of end-of-segment flight)
        # exp2j: acquisition choice. "table" = the paper's terminal-payoff
        # bracket rho*(b); "ei" = expected improvement over the incumbent
        # -- the payoff an OPTIMIZER actually collects, since it keeps the
        # running best and an unspent call is worth nothing at the end.
        # This is 1-D Bayesian optimization on the OU line: probe at
        # correlation rho has X ~ N(b rho, 1 - rho^2), and
        # EI(rho) = sigma phi(delta/sigma) - delta Phi(-delta/sigma) with
        # delta = b(1 - rho), sigma = sqrt(1 - rho^2). rho = 0 IS the
        # global fresh draw, so maximizing EI over [0, 1) endogenizes the
        # local-vs-global choice (dlib's MaxLIPO+TR architecture, with a
        # probabilistic bound in place of the Lipschitz one). ei_margin:
        # go global unless the local probe's EI beats the fresh draw's by
        # this factor -- "don't waste a call locally when the difference
        # is likely small."
        self.placement = placement
        self.ei_margin = ei_margin
        # exp2l: "linear" standardizes by running mean/std -- wrong when
        # the landscape is a monotone warp of the Gaussian field (on
        # actual exp(OU) the values are lognormal and one peak dominates
        # the std). "rank" Gaussianizes by normal scores, restoring the
        # model's N(0,1) marginal under ANY monotone warp (Gaussian
        # copula view); increments for the kappa fit use the same map.
        self.standardize = standardize

    _EI_RHO_GRID = np.linspace(0.0, 0.995, 200)

    def _ei_rho(self, b):
        """EI-optimal probe correlation, with the fresh draw (rho=0) as
        the standing rival. Returns 0.0 when the model's local edge is
        within the margin -- the call goes global instead."""
        rho = self._EI_RHO_GRID
        delta = b * (1.0 - rho)
        sig = np.sqrt(1.0 - rho**2)
        z = delta / np.maximum(sig, 1e-12)
        phi = np.exp(-0.5 * z * z) / np.sqrt(2 * np.pi)
        big_phi = 0.5 * (1.0 + _erf(z / np.sqrt(2.0)))
        ei = sig * phi - delta * (1.0 - big_phi)
        i = int(np.argmax(ei))
        if ei[i] <= self.ei_margin * ei[0]:
            return 0.0  # local edge too small: spend the call globally
        return float(rho[i])

    def _stats(self):
        if len(self.values) < 2:
            return 0.0, 1.0
        m = float(np.mean(self.values))
        s = float(np.std(self.values))
        return m, (s if s > 1e-12 else 1.0)

    def _make_std(self):
        """The value -> standardized-X map. Rank mode: normal scores
        (Gaussian copula), exact N(0,1) marginal under any monotone
        warp of the field; linear mode: running mean/std."""
        if self.standardize == "rank" and len(self.values) >= 4:
            vals = np.sort(np.asarray(self.values, dtype=float))
            n = len(vals)

            def x_of(f):
                k = float(np.searchsorted(vals, f, side="left"))
                q = (n - k + 0.5) / (n + 1.0)
                return float(_ndtri(min(max(q, 1e-12), 1 - 1e-12)))

            return x_of
        m, s = self._stats()
        return lambda f: (m - f) / s

    def _fit_kappa(self):
        """Variogram fit robust to the chi^2_1 tail: pairs are stored raw
        and standardized with the CURRENT stats (early pairs measured
        against a degenerate std would otherwise poison the fit), binned
        by distance, and the per-bin median increment is matched to its
        OU expectation 2(1-e^{-kappa D}) * med[chi^2_1]."""
        if len(self.pairs) < 8 or not self.adapt_kappa:
            return
        x_of = self._make_std()
        pairs = self.pairs[-256:]
        dist = np.array([q[0] for q in pairs])
        sq = np.array([x_of(q[1]) - x_of(q[2]) for q in pairs]) ** 2
        edges = np.geomspace(max(dist.min(), 1e-5), dist.max() + 1e-12, 9)
        dmid, dmed = [], []
        for a, b in zip(edges[:-1], edges[1:]):
            mask = (dist >= a) & (dist <= b)
            if mask.sum() >= 2:
                dmid.append(np.median(dist[mask]))
                dmed.append(np.median(sq[mask]))
        if len(dmid) < 3:
            return
        dmid, dmed = np.array(dmid), np.array(dmed)
        model = (
            2.0 * self.CHI2_MEDIAN * (1.0 - np.exp(-np.outer(self.KAPPA_GRID, dmid)))
        )
        sse = ((model - dmed[None, :]) ** 2).sum(axis=1)
        self.kappa = float(self.KAPPA_GRID[int(np.argmin(sse))])

    def __call__(self, budget, p, fp, v, rng):
        lo, hi = alpha_range(p, v)
        if hi - lo < 1e-9 or budget.remaining() <= 0:
            return p, fp
        std = self._make_std()  # minimize f == maximize X
        b = std(fp)
        kap = self.kappa

        # The bracket goes to the side with more room; anchor is alpha=0.
        side = 1.0 if hi >= -lo else -1.0
        room_fwd = hi if side > 0 else -lo  # room on the bracket side
        room_back = -lo if side > 0 else hi  # room on the other side
        if room_fwd < 1e-9:
            return p, fp

        # Shot 2: bracket at the three-shot optimal correlation. A run of
        # barren lines means the observed spread near the anchor is
        # negligible, in which case every placement ties in the model and
        # the tie breaks toward the flee branch (the stationary OU model
        # cannot see a nonstationary plateau; b measured against a
        # collapsed sample std is an artifact, not an exceptional anchor).
        if self.stall >= 3:
            r = 0.0
        elif self.placement == "ei":
            r = self._ei_rho(b)
        else:
            r = rho_star(b)
        if r <= 0.0:
            t1 = rng.uniform(0.4, 1.0) * room_fwd if self.uniform_flee else room_fwd
        else:
            t1 = min(-np.log(r) / kap, room_fwd)
        if t1 < 1e-9:
            return p, fp
        alpha1 = side * t1
        f1 = budget(p + alpha1 * v)
        self.values.append(f1)
        self.pairs.append((t1, fp, f1))
        d_val = std(f1)
        best_a, best_f = (alpha1, f1) if f1 < fp else (0.0, fp)

        if budget.remaining() > 0 and not self.skip_third:
            # Shot 3: best of stay (either anchor), exterior, interior.
            rho = float(np.exp(-kap * t1))
            zb, zd = zeta(b), zeta(d_val)
            vin, x_root = interior_optimum(b, d_val, rho)
            alpha2 = None  # None == stay: no third evaluation
            if vin > max(zb, zd):
                alpha2 = side * (-np.log(x_root) / kap)  # interior point
            else:
                y, base = (b, 0.0) if zb >= zd else (d_val, alpha1)
                if y <= 1.0:
                    # exterior ray past the winning anchor, away from the
                    # bracket; flee (y <= 0) goes as far as the cube allows
                    away = -side if base == 0.0 else side
                    max_room = room_back if base == 0.0 else max(room_fwd - t1, 0.0)
                    step = max_room if y <= 0.0 else min(-np.log(y) / kap, max_room)
                    if step > 1e-9:
                        alpha2 = base + away * step
            if alpha2 is not None:
                alpha2 = float(np.clip(alpha2, lo, hi))
                if abs(alpha2) > 1e-9 and abs(alpha2 - alpha1) > 1e-9:
                    f2 = budget(p + alpha2 * v)
                    self.values.append(f2)
                    self.pairs.append((abs(alpha2 - alpha1), f1, f2))
                    if f2 < best_f:
                        best_a, best_f = alpha2, f2
        self._fit_kappa()
        tol = 1e-12 + 1e-9 * abs(fp)
        self.stall = 0 if best_f < fp - tol else self.stall + 1
        return np.clip(p + best_a * v, 0, 1), best_f


# ---------------------------------------------------------------------------
# Shared outer loop
# ---------------------------------------------------------------------------


def iterated_line_search(objective, n_dim, n_trials, inner, seed):
    """One outer loop for every method: start at a common point, walk a
    common random-direction stream, hand each line to `inner`, move to
    the line's best. Returns (best_value, best_x, evaluations)."""
    rng_start = np.random.default_rng(seed)
    rng_dirs = np.random.default_rng(10_000 + seed)
    budget = Budget(objective, n_trials)
    p = np.asarray(rng_start.uniform(0.1, 0.9, n_dim))
    fp = budget(p)
    if isinstance(inner, GrassInner):
        inner.values.append(fp)
    while budget.remaining() > 0:
        v = rng_dirs.normal(size=n_dim)
        n = np.linalg.norm(v)
        if n < 1e-12:
            continue
        v /= n
        p, fp = inner(budget, p, fp, v, rng_dirs)
    return budget.best_value, budget.best_x, budget.evaluations


def random_search(objective, n_dim, n_trials, seed):
    rng = np.random.default_rng(seed)
    budget = Budget(objective, n_trials)
    while budget.remaining() > 0:
        budget(rng.uniform(0, 1, n_dim))
    return budget.best_value, budget.best_x, budget.evaluations
