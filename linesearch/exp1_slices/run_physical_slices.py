"""Slice roughness of humpday's PHYSICAL demos -- collision/chaos
simulators (bowling, plinko, pool, trebuchet, mini golf, curling).
Hypothesis (Peter): unlike the smooth classic/horse objectives, the
physical landscapes are natively rough -- p well below 2, possibly
near OU (p=1) -- with no Morton trick needed."""
import importlib
import sys
import numpy as np
sys.path.insert(0, "/Users/petercotton/github/humpday")
sys.path.insert(0, "/Users/petercotton/github/humpday/example_applications")
from run_slices import variogram_p

DEMOS = ["bowling", "plinko_funnel", "pool", "trebuchet",
         "mini_golf", "curling"]


def get_objective(mod):
    for name in ("objective", "simulate_throw_objective"):
        if hasattr(mod, name):
            return getattr(mod, name)
    # fall back to any callable taking u and returning float
    for name in ("throw_range", "finish_distance", "stop_distance"):
        if hasattr(mod, name):
            return getattr(mod, name)
    raise AttributeError("no objective found")


if __name__ == "__main__":
    rng = np.random.default_rng(5)
    for demo in DEMOS:
        try:
            mod = importlib.import_module(f"{demo}.problem")
            obj = get_objective(mod)
            d = mod.N_DIM
            ps = []
            for _ in range(6):
                x0 = rng.uniform(0.15, 0.85, d)
                v = rng.normal(size=d); v /= np.linalg.norm(v)
                ts = np.linspace(-0.3, 0.3, 257)
                pts = np.clip(x0[None, :] + ts[:, None] * v[None, :],
                              0, 1)
                vals = np.array([float(obj(list(p))) for p in pts])
                if np.std(vals) < 1e-12:
                    continue
                ps.append(variogram_p(vals, 0.6 / 257))
            med = np.nanmedian(ps) if ps else float("nan")
            print(f"  {demo:14s} (d={d}) median p = {med:.2f}  "
                  f"({len(ps)} usable slices)")
        except Exception as e:
            print(f"  {demo}: ERROR {str(e)[:70]}")
