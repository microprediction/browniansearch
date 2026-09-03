"""Are 1-D slices of DFO objectives OU-like? Measure the
powered-exponential roughness exponent p.

For a GP with kernel exp(-|D/l|^p), the small-lag variogram obeys
E[(f(x+D)-f(x))^2] ~ D^p, so the log-log variogram slope estimates
p: p=2 smooth (squared-exponential regime, classical line search
fine), p=1 Ornstein-Uhlenbeck (the grass paper's home), p<1 rougher.

Hypothesis: direct random-line slices of classic test objectives are
smooth (p ~ 2); Morton/space-filling-curve composition -- the
standard 1-D-ification, and a Hoelder-1/d map -- yields p ~ 2/d:
OU exactly at d=2, rougher above.
"""
import sys
import numpy as np

sys.path.insert(0, "/Users/petercotton/github/humpday")
from humpday.objectives.classic import (
    schwefel_on_cube, griewank_on_cube, rastrigin_on_cube,
    rosenbrock_on_cube, paviani_on_cube)

OBJECTIVES = [("schwefel", schwefel_on_cube),
              ("griewank", griewank_on_cube),
              ("rastrigin", rastrigin_on_cube),
              ("rosenbrock", rosenbrock_on_cube)]


def variogram_p(vals, dx, nlags=12):
    """log-log slope of E[(f(x+D)-f(x))^2] vs D at small lags."""
    lags = np.unique(np.geomspace(1, len(vals) // 8, nlags).astype(int))
    vg = [np.mean((vals[k:] - vals[:-k]) ** 2) for k in lags]
    vg = np.array(vg)
    good = vg > 0
    if good.sum() < 3:
        return np.nan
    return float(np.polyfit(np.log(lags[good] * dx),
                            np.log(vg[good]), 1)[0])


def direct_slice_p(obj, d, rng, npts=1025):
    x0 = rng.uniform(0.1, 0.9, d)
    v = rng.normal(size=d); v /= np.linalg.norm(v)
    tmax = 0.4
    ts = np.linspace(-tmax, tmax, npts)
    pts = np.clip(x0[None, :] + ts[:, None] * v[None, :], 0, 1)
    vals = np.array([obj(list(p)) for p in pts])
    return variogram_p(vals, 2 * tmax / npts)


def morton_map(u, d, bits=20):
    """u in [0,1) -> [0,1)^d by bit de-interleaving (z-curve inverse
    image: 1-D parameter sweeping the cube)."""
    key = int(u * (1 << (bits * d)))
    coords = [0] * d
    for b in range(bits):
        for j in range(d):
            coords[j] |= ((key >> (b * d + j)) & 1) << b
    return [c / (1 << bits) for c in coords]


def morton_slice_p(obj, d, rng, npts=8193):
    u0 = rng.uniform(0, 1 - 1 / 64)
    us = u0 + np.linspace(0, 1 / 64, npts)   # a window of the curve
    vals = np.array([obj(morton_map(u, d)) for u in us])
    return variogram_p(vals, (1 / 64) / npts)


if __name__ == "__main__":
    rng = np.random.default_rng(7)
    print("== direct random-line slices (d=3) ==")
    for name, obj in OBJECTIVES:
        ps = [direct_slice_p(obj, 3, rng) for _ in range(12)]
        print(f"  {name:12s} median p = {np.nanmedian(ps):.2f}  "
              f"(iqr {np.nanpercentile(ps,25):.2f}-"
              f"{np.nanpercentile(ps,75):.2f})")
    print("== Morton-composed slices: hypothesis p ~ 2/d ==")
    for d in (2, 3, 4):
        row = []
        for name, obj in OBJECTIVES:
            ps = [morton_slice_p(obj, d, rng) for _ in range(6)]
            row.append(f"{name} {np.nanmedian(ps):.2f}")
        print(f"  d={d} (predict {2/d:.2f}): " + "  ".join(row))
