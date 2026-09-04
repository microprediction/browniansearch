"""exp2h: the paper's closing conjecture, tested in its native
habitat. The grass paper conjectures a two-phase k-shot policy: "step
out past the running best while values climb, then refine between the
two best once a good region is bracketed, with the pitchfork
inherited by the refinement phase" and "no irreversible switch, since
an adverse interior observation can make leaving attractive again."

Here that policy is implemented and raced on genuine 1-D rough
landscapes (Morton-composed classics at d=2, the p~0.75 OU regime,
and d=3, rougher) against golden section, Brent, random sampling, and
the iterated-line grass2U restricted to 1-D. Budget k = 5..40
evaluations of f on [0,1]; kappa and standardization estimated online
as everywhere else in exp2.
"""

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/Users/petercotton/github/humpday")
sys.path.insert(0, os.path.join(HERE, "..", "exp1_slices"))

from run_slices import morton_map  # noqa: E402
from ou3_linesearch import (  # noqa: E402
    GrassInner,
    brent_inner,
    golden_inner,
    interior_optimum,
    iterated_line_search,
    rho_star,
    zeta,
)

from humpday.objectives.classic import (  # noqa: E402
    griewank_on_cube,
    rastrigin_on_cube,
    schwefel_on_cube,
)


def fit_kappa_1d(xs, fs, grid=np.geomspace(2.0, 200.0, 60)):
    """Binned-median variogram fit over all pairs (same estimator family
    as GrassInner._fit_kappa, applied to the 1-D evaluation cloud)."""
    n = len(xs)
    if n < 5:
        return 20.0
    s = np.std(fs)
    if s < 1e-12:
        return 20.0
    X = np.asarray(xs)
    F = np.asarray(fs) / s
    ii, jj = np.triu_indices(n, k=1)
    dist = np.abs(X[ii] - X[jj])
    sq = (F[ii] - F[jj]) ** 2
    keep = dist > 1e-9
    dist, sq = dist[keep], sq[keep]
    if len(dist) < 4:
        return 20.0
    edges = np.geomspace(max(dist.min(), 1e-5), dist.max() + 1e-12, 9)
    dmid, dmed = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (dist >= a) & (dist <= b)
        if m.sum() >= 2:
            dmid.append(np.median(dist[m]))
            dmed.append(np.median(sq[m]))
    if len(dmid) < 3:
        return 20.0
    dmid, dmed = np.array(dmid), np.array(dmed)
    model = 2.0 * 0.4549364 * (1.0 - np.exp(-np.outer(grid, dmid)))
    sse = ((model - dmed[None, :]) ** 2).sum(axis=1)
    return float(grid[int(np.argmin(sse))])


def two_phase(obj, k, seed):
    """The conjectured k-shot policy on [0,1]."""
    rng = np.random.default_rng(seed)
    xs, fs = [], []

    def ev(u):
        u = float(np.clip(u, 0.0, 1.0))
        f = float(obj(u))
        xs.append(u)
        fs.append(f)
        return f

    x = float(rng.uniform(0.1, 0.9))
    ev(x)
    direction = 1.0 if x < 0.5 else -1.0  # step-out heads for open country
    phase = "out"
    stall = 0  # same plateau tie-break as GrassInner: barren stretches flee
    while len(fs) < k:
        if stall >= 3:
            fbest = min(fs)
            ev(rng.uniform(0.0, 1.0))
            stall = 0 if fs[-1] < fbest else stall
            phase = "out"
            continue
        kappa = fit_kappa_1d(xs, fs)
        m, s = float(np.mean(fs)), float(np.std(fs))
        s = s if s > 1e-12 else 1.0
        order = np.argsort(fs)  # ascending f: best first (minimizing)
        xb, fb = xs[order[0]], fs[order[0]]
        b = (m - fb) / s
        if phase == "out":
            # step past the running best by the explore distance
            r = rho_star(b)
            step = (1.0 if r <= 0 else min(-np.log(r) / kappa, 1.0)) * direction
            u = xb + step
            if u < 0.0 or u > 1.0:
                direction = -direction
                u = float(np.clip(xb + step * -1.0, 0.0, 1.0))
            f = ev(u)
            stall = 0 if f < fb else stall + 1
            if f > fb and len(fs) >= 3:
                phase = "refine"  # the climb stopped: bracket and refine
        else:
            # refine between the two best; pitchfork via the quartic
            x2, f2 = xs[order[1]], fs[order[1]]
            lo, hi = (xb, x2) if xb < x2 else (x2, xb)
            if hi - lo < 1e-6:
                phase = "out"
                continue
            rho = float(np.exp(-kappa * (hi - lo)))
            bb, dd = (m - fb) / s, (m - f2) / s
            vin, x_root = interior_optimum(bb, dd, rho)
            if vin > max(zeta(bb), zeta(dd)):
                # interior placement measured from the better anchor
                t2 = -np.log(x_root) / kappa
                u = xb + (t2 if x2 > xb else -t2)
                f = ev(u)
                stall = 0 if f < fb else stall + 1
                if (m - f) / s < 0.0:  # adverse interior observation:
                    phase = "out"  # leaving becomes attractive again
            else:
                phase = "out"  # verdict says exterior: step out again
                direction = 1.0 if x2 < xb else -1.0  # past the better end
    return float(np.min(fs))


def run_1d(method, obj, k, seed):
    if method == "twophase":
        return two_phase(obj, k, seed)
    if method == "grass2U":
        inner = GrassInner(skip_third=True, uniform_flee=True)
        return float(iterated_line_search(lambda v: obj(v[0]), 1, k, inner, seed)[0])
    if method == "golden":
        inner = golden_inner(k)
        return float(iterated_line_search(lambda v: obj(v[0]), 1, k, inner, seed)[0])
    if method == "brent":
        inner = brent_inner(k)
        return float(iterated_line_search(lambda v: obj(v[0]), 1, k, inner, seed)[0])
    if method == "random":
        rng = np.random.default_rng(seed)
        return float(min(obj(float(rng.uniform())) for _ in range(k)))
    raise ValueError(method)


def morton_obj(base, d):
    return lambda u: float(base(morton_map(min(max(u, 0.0), 1.0 - 1e-12), d)))


PROBLEMS = [
    ("morton_schwefel_d2", morton_obj(schwefel_on_cube, 2)),
    ("morton_rastrigin_d2", morton_obj(rastrigin_on_cube, 2)),
    ("morton_griewank_d2", morton_obj(griewank_on_cube, 2)),
    ("morton_schwefel_d3", morton_obj(schwefel_on_cube, 3)),
]
METHODS = ["twophase", "grass2U", "golden", "brent", "random"]
KS = [5, 10, 20, 40]
SEEDS = 48

if __name__ == "__main__":
    out = {"seeds": SEEDS, "ks": KS, "problems": {}}
    for name, obj in PROBLEMS:
        out["problems"][name] = {}
        for k in KS:
            t0 = time.time()
            rows = {m: [run_1d(m, obj, k, s) for s in range(SEEDS)] for m in METHODS}
            med = {m: float(np.median(v)) for m, v in rows.items()}
            out["problems"][name][k] = {"results": rows, "medians": med}
            order = sorted(med, key=med.get)
            rank = order.index("twophase") + 1
            print(
                f"{name:20s} k={k:2d} twophase rank {rank}/5  "
                + "  ".join(f"{m}={med[m]:.4g}" for m in order)
                + f"  ({time.time() - t0:4.1f}s)",
                flush=True,
            )
    with open(os.path.join(HERE, "kshot_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote kshot_results.json")
