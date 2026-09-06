"""Corrected numerics for the grass paper (post-review).

Interior optima via the exact stationarity quartic
  x^4 - (b - rho d) x^3 + rho (d - rho b) x - rho^2 = 0
(roots in (rho,1) plus nothing else needed: end limits are covered
by zeta of the anchors). Outer integral over the second observation
by adaptive quadrature (scipy quad), rho optimized by bounded scalar
minimization. Produces the corrected Table 1 (interior-option gain,
with the comparison policy properly named interior-excluded), the
widening decomposition at b=0.5, the exact flee limit, and the gain
curve for the figure's right panel.
"""
import json
import os

import numpy as np
from scipy.integrate import quad
from scipy.optimize import minimize_scalar
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))


def zeta(y):
    return 0.5 if y < 0 else ((y * y + 1) / 2 if y <= 1 else float(y))


def sup_interior(b, d, rho):
    """Exact: evaluate f at real quartic roots in (rho, 1)."""
    coeffs = [1.0, -(b - rho * d), 0.0, rho * (d - rho * b),
              -rho ** 2]
    best = -np.inf
    for r in np.roots(coeffs):
        if abs(r.imag) < 1e-9 and rho < r.real < 1:
            x = r.real
            lam = rho / x
            den = 1 - rho * rho
            mu = (x * (1 - lam ** 2) * b
                  + lam * (1 - x ** 2) * d) / den
            nu = (1 - x ** 2) * (1 - lam ** 2) / den
            best = max(best, mu + nu / 2)
    return best


def V(b, d, rho, with_interior=True):
    v = max(zeta(b), zeta(d))
    if with_interior:
        v = max(v, sup_interior(b, d, rho))
    return v


def value(b, rho, with_interior=True):
    sd = np.sqrt(1 - rho ** 2)
    f = lambda z: norm.pdf(z) * np.exp(
        V(b, b * rho + sd * z, rho, with_interior))
    ex, _ = quad(f, -10, 10, limit=300, epsabs=1e-11, epsrel=1e-11)
    return float(np.log(ex))


def opt_rho(b, with_interior=True):
    r = minimize_scalar(lambda rho: -value(b, rho, with_interior),
                        bounds=(1e-3, 0.999), method="bounded",
                        options=dict(xatol=1e-5))
    return float(r.x), float(-r.fun)




def make_figure():
    """The paper's figure: exact symmetric region + interior-option
    gain curve (adaptive quadrature, quartic-exact interior)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.6))
    rr = np.linspace(0.005, 0.995, 400)
    s = np.sqrt(rr)
    lo = s * (2 - np.sqrt(2 * (1 - rr))) / (1 + rr)
    upper = (1 + rr) / (1 - rr)
    bif = 2 * s / (1 - rr)
    ax = axes[0]
    ax.fill_between(rr, lo, np.minimum(upper, 1.6), alpha=0.25,
                    color="tab:blue", label="revisit the interior")
    ax.plot(rr, lo, "tab:blue", lw=1.2)
    ax.plot(rr, np.minimum(upper, 1.6), "tab:blue", lw=1.2)
    ax.plot(rr, np.minimum(bif, 1.6), "tab:green", lw=1.0, ls=":",
            label=r"pitchfork $b=b_{\mathrm{p}}$ (middle $\to$ ends)")
    ax.plot(rr, rr, "k--", lw=0.9,
            label=r"$\rho=b$ (two-shot bracket)")
    ax.set_xlabel(r"bracket correlation $\rho=e^{-\kappa t_1}$")
    ax.set_ylabel(r"anchor value $b=d$")
    ax.set_ylim(0, 1.6)
    ax.set_title("the symmetric revisit region, exactly")
    ax.legend(frameon=False, fontsize=8)
    ax = axes[1]
    bs = np.linspace(0.05, 1.3, 26)
    gains = []
    for b in bs:
        _, vw = opt_rho(b, True)
        _, v0 = opt_rho(b, False)
        gains.append((np.exp(vw) - np.exp(v0)) / np.exp(v0) * 100)
    ax.plot(bs, gains, "tab:red", lw=1.4)
    ax.axhline(0, color="k", lw=0.6)
    ax.set_xlabel(r"first discovered value $b$")
    ax.set_ylabel("value of the interior option (%)")
    ax.set_title("what excluding interior placement costs")
    fig.tight_layout()
    os.makedirs(os.path.join(HERE, "figures"), exist_ok=True)
    fig.savefig(os.path.join(HERE, "figures", "phase.pdf"))
    print("wrote figures/phase.pdf")


if __name__ == "__main__":
    out = {}
    print("== corrected Table 1: adaptive integration, exact "
          "interior ==")
    rows = []
    for b in (0.1, 0.3, 0.5, 0.7, 0.83, 0.9, 1.2):
        rw, vw = opt_rho(b, True)
        r0, v0 = opt_rho(b, False)
        gain = (np.exp(vw) - np.exp(v0)) / np.exp(v0) * 100
        rows.append(dict(b=b, rho_with=rw, val_with=vw,
                         rho_wo=r0, val_wo=v0, gain_pct=gain))
        print(f"  b={b:4.2f}: rho*={rw:.5f} value={vw:.5f} | "
              f"interior-excluded rho*={r0:.5f} value={v0:.5f} | "
              f"gain {gain:.3f}%")
    out["table"] = rows
    exact_flee = 0.5 + np.log(1 + 1 / np.sqrt(2 * np.pi))
    print(f"  b<0 (flee, rho->0 limit, exact): {exact_flee:.6f}")
    out["flee_exact"] = exact_flee
    print("\n== widening decomposition at b=0.5 ==")
    rw, _ = opt_rho(0.5, True)
    r0, _ = opt_rho(0.5, False)
    print(f"  two-shot rho = 0.5; interior-excluded rho* = {r0:.5f};"
          f" interior-allowed rho* = {rw:.5f}")
    out["widening"] = dict(two_shot=0.5, excluded=r0, allowed=rw)
    json.dump(out, open(os.path.join(HERE, "results2.json"), "w"),
              indent=2)
    print("wrote results2.json")
    make_figure()
