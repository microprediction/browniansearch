"""Break and repair the middle-optimality lemma.

Symmetric bracket d=b, correlation rho, interior point at
x = lam2 in (rho,1), lam = rho/x. Log-utility
  f(x) = b(x + rho/x)/(1+rho) + (1-x^2)(1-rho^2/x^2)/(2(1-rho^2)).
Claims to verify:
 1. f'(x) x^3 (1+rho)(1-rho^2) factorizes so that critical points
    solve (x^2-rho)(x^2 - b(1-rho)x + rho) = 0: the middle sqrt(rho)
    always, and an off-middle pair iff b(1-rho) >= 2 sqrt(rho),
    i.e. b >= sinh(2 tau) with tanh(tau) = sqrt(rho).
 2. Second derivative at the middle changes sign at the same
    threshold: middle is a local max iff b < sinh(2 tau).
 3. Consequence for the paper's boundary: for rho < 3-2sqrt(2)
    (~0.1716) and b above the bifurcation, the off-middle optimum
    can beat zeta(b) where the middle does not -- the true symmetric
    revisit region strictly exceeds the quadratic region.
"""
import numpy as np

def f(x, b, rho):
    lam = rho / x
    mu = b * (x + lam) / (1 + rho)
    nu = (1 - x * x) * (1 - lam * lam) / (1 - rho * rho)
    return mu + nu / 2

def zeta(y):
    return 0.5 if y < 0 else ((y * y + 1) / 2 if y <= 1 else y)

def crits(b, rho):
    """Roots of x^2 - b(1-rho)x + rho = 0 in (rho, 1)."""
    disc = b * b * (1 - rho) ** 2 - 4 * rho
    if disc < 0:
        return []
    r = np.sqrt(disc)
    return [x for x in (((b * (1 - rho) - r) / 2),
                        ((b * (1 - rho) + r) / 2))
            if rho < x < 1]

if __name__ == "__main__":
    print("== claim 1+2: bifurcation at b = sinh(2 tau) = "
          "2 sqrt(rho)/(1-rho) ==")
    for rho in (0.04, 0.1, 0.3, 0.5):
        bstar = 2 * np.sqrt(rho) / (1 - rho)
        for b in (0.8 * bstar, 1.2 * bstar):
            xs = np.linspace(rho + 1e-6, 1 - 1e-6, 40001)
            fv = f(xs, b, rho)
            xopt = xs[np.argmax(fv)]
            mid = np.sqrt(rho)
            cp = crits(b, rho)
            kind = ("middle" if abs(xopt - mid) < 2e-4
                    else "off-middle")
            pred = "middle" if b < bstar else "off-middle"
            ok = "OK" if kind == pred else "MISMATCH"
            cptxt = (f" analytic off-mid x={cp[-1]:.4f}"
                     f" (grid {xopt:.4f})" if cp else "")
            print(f"  rho={rho:.2f} b={b:.3f} (b*={bstar:.3f}): "
                  f"optimum {kind} [{ok}]{cptxt}")
    print()
    print("== claim 3: true revisit region exceeds the quadratic at "
          "small rho ==")
    for rho, b in ((0.04, 0.80), (0.04, 0.90), (0.08, 0.85),
                   (0.1716, 0.95)):
        xs = np.linspace(rho + 1e-6, 1 - 1e-6, 40001)
        best = float(np.max(f(xs, b, rho)))
        midv = f(np.sqrt(rho), b, rho)
        z = zeta(b)
        s = np.sqrt(rho)
        bhi = s * (2 + np.sqrt(2 * (1 - rho))) / (1 + rho)
        print(f"  rho={rho:.4f} b={b:.2f}: quadratic upper edge "
              f"b_+={bhi:.3f}; middle {midv:.4f}, best interior "
              f"{best:.4f}, zeta {z:.4f} -> "
              f"{'REVISIT (off-middle)' if best > z else 'go forth'}"
              f"{' though middle loses' if best > z > midv else ''}")
    print()
    print("== exact symmetric boundary vs quadratic (numeric sweep) ==")
    from scipy.optimize import brentq
    for rho in (0.02, 0.05, 0.1716, 0.3, 0.5):
        xs = np.linspace(rho + 1e-6, 1 - 1e-6, 20001)
        g = lambda b: float(np.max(f(xs, b, rho))) - zeta(b)
        # lower edge
        try:
            blo_true = brentq(g, 1e-4, 1.0)
        except ValueError:
            blo_true = np.nan
        s = np.sqrt(rho)
        blo_q = s * (2 - np.sqrt(2 * (1 - rho))) / (1 + rho)
        # upper edge (within [blo,1.6] if it exists)
        try:
            bhi_true = brentq(g, blo_true + 1e-3, 1.6)
        except ValueError:
            bhi_true = np.inf
        bhi_q = s * (2 + np.sqrt(2 * (1 - rho))) / (1 + rho)
        print(f"  rho={rho:.4f}: lower true {blo_true:.4f} vs quad "
              f"{blo_q:.4f}; upper true "
              f"{bhi_true if bhi_true != np.inf else float('inf'):.4f}"
              f" vs quad {bhi_q:.4f}")
