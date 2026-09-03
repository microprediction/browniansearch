"""All measured numbers and the figure for the Go Forth paper.

Model: X zero-mean unit-variance OU, kernel exp(-kappa|s-t|).
Samples at 0 (value b), t1 (value d), then a final point t2; payoff
E[exp(X_{t2})] = exp(mu + nu/2). rho = exp(-kappa t1) is the bracket
correlation. Inside the bracket, lam2/lam are the correlations to
the two ends, lam2*lam = rho.

Produces:
  1. the symmetric-case boundary b_-(rho), b_+(rho) (closed form)
     and a spot-check table inside-middle vs best-outside;
  2. the three-shot value with and without the revisit option,
     optimal rho, for a grid of b (Gauss-Hermite over d);
  3. flee check for b < 0 (value maximized as rho -> 0);
  4. figures/phase.pdf: the revisit region and the value of
     revisiting.
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def zeta(y):
    """Best outside log-value from an anchor with value y."""
    y = np.asarray(y, float)
    return np.where(y < 0, 0.5,
                    np.where(y <= 1, (y * y + 1) / 2, y))


def bridge(b, d, lam2, lam):
    rho = lam2 * lam
    den = 1 - rho ** 2
    mu = (lam2 * (1 - lam ** 2) * b + lam * (1 - lam2 ** 2) * d) / den
    nu = (1 - lam2 ** 2) * (1 - lam ** 2) / den
    return mu, nu


def best_inside(b, d, rho, ngrid=400):
    lam2 = np.linspace(rho + 1e-9, 1 - 1e-9, ngrid)
    lam = rho / lam2
    mu, nu = bridge(b, d, lam2, lam)
    u = mu + nu / 2
    i = int(np.argmax(u))
    return float(u[i]), float(lam2[i])


def middle_value(b, rho):
    s = np.sqrt(rho)
    return 2 * b * s / (1 + rho) + (1 - rho) / (2 * (1 + rho))


def boundary(rho):
    """Closed-form roots of b^2(1+rho) - 4 b sqrt(rho) + 2 rho = 0:
    inside-middle beats (b^2+1)/2 iff b between the roots."""
    s = np.sqrt(rho)
    disc = np.sqrt(2 * rho * (1 - rho))
    lo = (2 * s - np.sqrt(2) * s * np.sqrt(1 - rho)) / (1 + rho)
    hi = (2 * s + np.sqrt(2) * s * np.sqrt(1 - rho)) / (1 + rho)
    return lo, hi


def three_shot(b, rho, nq=61, with_inside=True):
    """E_d[ max(zeta(b), zeta(d), best_inside) ] by Gauss-Hermite."""
    z, w = np.polynomial.hermite_e.hermegauss(nq)
    w = w / w.sum()
    dvals = b * rho + np.sqrt(1 - rho ** 2) * z
    vals = []
    for d in dvals:
        v = max(float(zeta(b)), float(zeta(d)))
        if with_inside:
            vi, _ = best_inside(b, d, rho)
            v = max(v, vi)
        vals.append(np.exp(v))
    return float(np.log(np.dot(w, vals)))   # log of expected exp-value


if __name__ == "__main__":
    out = {}

    print("== symmetric slice: inside middle vs best outside, "
          "rho = b (two-shot-inherited bracket) ==")
    rows = []
    for b in (0.2, 0.3, 0.4, 0.45, 0.5, 0.7, 0.9):
        um = middle_value(b, b)
        uo = float(zeta(b))
        lo, hi = boundary(b)
        rows.append(dict(b=b, inside=um, outside=uo,
                         blo=float(lo), bhi=float(hi)))
        print(f"  b={b:.2f}: middle {um:.4f} vs zeta {uo:.4f}  "
              f"boundary at this rho: ({lo:.4f},{hi:.4f})  "
              f"{'REVISIT' if um > uo else 'go forth'}")
    out["symmetric"] = rows

    # crossover along rho = b
    from scipy.optimize import brentq
    f = lambda b: middle_value(b, b) - float(zeta(b))
    bstar = brentq(f, 0.2, 0.6)
    print(f"crossover along rho=b: b* = {bstar:.4f}")
    out["crossover_rho_eq_b"] = float(bstar)

    print("\n== three-shot value, optimal rho, and the worth of "
          "the revisit option ==")
    rows = []
    rhogrid = np.linspace(0.02, 0.98, 49)
    for b in (-0.5, 0.1, 0.3, 0.5, 0.7, 0.9, 1.2):
        vals = [three_shot(b, r) for r in rhogrid]
        i = int(np.argmax(vals))
        v_with = vals[i]
        v_wo = max(three_shot(b, r, with_inside=False)
                   for r in rhogrid)
        gain = (np.exp(v_with) - np.exp(v_wo)) / np.exp(v_wo)
        rows.append(dict(b=b, rho_opt=float(rhogrid[i]),
                         value=v_with, value_noback=v_wo,
                         gain_pct=float(gain * 100)))
        print(f"  b={b:+.1f}: rho* {rhogrid[i]:.2f}  value {v_with:.4f}"
              f"  no-revisit {v_wo:.4f}  revisit worth "
              f"{gain*100:.2f}%")
    out["three_shot"] = rows

    # figure
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    rr = np.linspace(0.005, 0.995, 400)
    lo, hi = boundary(rr)
    ax = axes[0]
    ax.fill_between(rr, lo, np.minimum(hi, 1.4), alpha=0.25,
                    color="tab:blue", label="revisit the bridge")
    ax.plot(rr, lo, "tab:blue", lw=1.2)
    ax.plot(rr, np.minimum(hi, 1.4), "tab:blue", lw=1.2)
    ax.plot(rr, rr, "k--", lw=0.9, label=r"$\rho=b$ (two-shot bracket)")
    ax.set_xlabel(r"bracket correlation $\rho=e^{-\kappa t_1}$")
    ax.set_ylabel(r"anchor value $b=d$")
    ax.set_ylim(0, 1.4)
    ax.set_title("where the bridge middle beats going forth")
    ax.legend(frameon=False, fontsize=8)
    ax = axes[1]
    bs = np.linspace(0.05, 1.3, 40)
    gains = []
    for b in bs:
        v = max(three_shot(b, r) for r in rhogrid[::2])
        v0 = max(three_shot(b, r, with_inside=False)
                 for r in rhogrid[::2])
        gains.append((np.exp(v) - np.exp(v0)) / np.exp(v0) * 100)
    ax.plot(bs, gains, "tab:red", lw=1.4)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xlabel(r"first discovered value $b$")
    ax.set_ylabel("value of the revisit option (%)")
    ax.set_title("what banning backtracking costs")
    fig.tight_layout()
    os.makedirs(os.path.join(HERE, "figures"), exist_ok=True)
    fig.savefig(os.path.join(HERE, "figures", "phase.pdf"))
    print("wrote figures/phase.pdf")

    json.dump(out, open(os.path.join(HERE, "results.json"), "w"),
              indent=2)
    print("wrote results.json")
