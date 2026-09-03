"""Try to break single-crossing at k=2.

State: bracket (b,d,rho), middle revealed v, TWO shots left (one
info sample, then the final placement anywhere). Stay = info sample
inside a sub-bracket; Exit = info sample outside an original end.
Both continuations depend on v (an exit may re-enter for the final
placement), so the k=1 proof of single crossing does not apply.
This probe computes stay2(v) - exit2(v) on a grid and counts sign
changes. One = threshold survives; more = broken.
"""
import numpy as np

NODES, WQ = np.polynomial.hermite_e.hermegauss(21)
WQ = WQ / WQ.sum()

def zeta(y):
    return 0.5 if y < 0 else ((y * y + 1) / 2 if y <= 1 else float(y))

def sup_int(p, q, r, ngrid=200):
    if r >= 1 - 1e-9:
        return max(p, q)
    x = np.linspace(r + 1e-9, 1 - 1e-9, ngrid)
    lam = r / x
    den = 1 - r * r
    mu = (x * (1 - lam ** 2) * p + lam * (1 - x ** 2) * q) / den
    nu = (1 - x ** 2) * (1 - lam ** 2) / den
    return float(np.max(mu + nu / 2))

def v_final(vals, rhos):
    """Frontier values vals[0..m] with adjacent correlations rhos:
    best final placement (interiors + two outer rays)."""
    best = max(zeta(vals[0]), zeta(vals[-1]))
    for i in range(len(rhos)):
        best = max(best, sup_int(vals[i], vals[i + 1], rhos[i]))
    return best

def bridge_mom(p, q, r, x):
    lam = r / x
    den = 1 - r * r
    mu = (x * (1 - lam ** 2) * p + lam * (1 - x ** 2) * q) / den
    nu = (1 - x ** 2) * (1 - lam ** 2) / den
    return mu, nu

def opt_info_inside(vals, rhos, seg, ngrid=13):
    """Info sample inside segment seg at position x; then final."""
    p, q, r = vals[seg], vals[seg + 1], rhos[seg]
    best = -np.inf
    for x in np.linspace(r + 0.02, 0.98, ngrid):
        mu, nu = bridge_mom(p, q, r, x)
        tot = 0.0
        for z, w in zip(NODES, WQ):
            wv = mu + np.sqrt(max(nu, 1e-12)) * z
            nv = vals[:seg + 1] + [wv] + vals[seg + 1:]
            nr = rhos[:seg] + [x, r / x] + rhos[seg + 1:]
            tot += w * np.exp(v_final(nv, nr))
        best = max(best, np.log(tot))
    return best

def opt_info_outside(vals, rhos, side, ngrid=13):
    """Info sample beyond an end at correlation lam; then final."""
    anchor = vals[0] if side == "L" else vals[-1]
    best = -np.inf
    for lam in np.linspace(0.05, 0.95, ngrid):
        mu, sd = anchor * lam, np.sqrt(1 - lam ** 2)
        tot = 0.0
        for z, w in zip(NODES, WQ):
            wv = mu + sd * z
            if side == "L":
                nv, nr = [wv] + vals, [lam] + rhos
            else:
                nv, nr = vals + [wv], rhos + [lam]
            tot += w * np.exp(v_final(nv, nr))
        best = max(best, np.log(tot))
    return best

def crossing_profile(b, d, rho, vgrid):
    s = np.sqrt(rho)
    diffs = []
    for v in vgrid:
        vals, rhos = [b, v, d], [s, s]
        stay = max(opt_info_inside(vals, rhos, 0),
                   opt_info_inside(vals, rhos, 1))
        exit_ = max(opt_info_outside(vals, rhos, "L"),
                    opt_info_outside(vals, rhos, "R"))
        diffs.append(stay - exit_)
    return np.array(diffs)

if __name__ == "__main__":
    for (b, d, rho) in ((0.7, 0.7, 0.5), (0.9, 0.5, 0.3),
                        (0.8, 0.8, 0.08)):
        vg = np.linspace(-1.0, 2.2, 25)
        df = crossing_profile(b, d, rho, vg)
        sign = np.sign(df)
        changes = int(np.sum(sign[1:] * sign[:-1] < 0))
        print(f"(b,d,rho)=({b},{d},{rho}): sign changes = {changes}")
        rows = "  ".join(f"{v:+.2f}:{x:+.3f}" for v, x in
                         list(zip(vg, df))[::3])
        print("   " + rows)
