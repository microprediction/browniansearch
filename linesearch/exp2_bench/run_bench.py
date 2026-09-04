"""exp2: head-to-head of inner line searches inside one outer DFO loop,
on humpday objectives split by measured slice roughness (exp1_slices).

Rough family (the OU rule's predicted home): bowling p=0.29,
plinko_funnel p=1.34, Morton-composed classic objectives at d=2
(p=0.71-0.79, the OU regime). Smooth controls (golden/Brent
territory, per the notes "and should be said so plainly"): pool and
mini_golf (p=1.91-1.99) and rosenbrock d=3 (direct slices p~2).

Protocol: every method shares the same outer loop, start point, and
random-direction stream per seed; only the inner line search differs.
Fixed total evaluation budget; the grass rule spends 1-2 evaluations
per line (a "stay" verdict spends one), golden and Brent spend their
usual more. Metric: best value found, median and IQR over seeds.
"""

import importlib
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/Users/petercotton/github/humpday")
sys.path.insert(0, "/Users/petercotton/github/humpday/example_applications")
sys.path.insert(0, os.path.join(HERE, "..", "exp1_slices"))

from run_slices import morton_map  # noqa: E402
from ou3_linesearch import (  # noqa: E402
    GrassInner,
    brent_inner,
    golden_inner,
    iterated_line_search,
    random_search,
)

from humpday.objectives.classic import (  # noqa: E402
    rastrigin_on_cube,
    rosenbrock_on_cube,
    schwefel_on_cube,
)


def physical(demo):
    mod = importlib.import_module(f"{demo}.problem")
    for name in ("objective", "simulate_throw_objective"):
        if hasattr(mod, name):
            return getattr(mod, name), mod.N_DIM
    raise AttributeError(demo)


def morton_1d(obj, d):
    def f(x):
        return float(obj(morton_map(float(x[0]), d)))

    return f


def build_problems():
    bowling, d_bowl = physical("bowling")
    plinko, d_plinko = physical("plinko_funnel")
    pool, d_pool = physical("pool")
    mini_golf, d_golf = physical("mini_golf")
    return [
        # name, objective, n_dim, family, seeds
        ("bowling", bowling, d_bowl, "rough", 12),
        ("plinko_funnel", plinko, d_plinko, "rough", 24),
        ("morton_schwefel_d2", morton_1d(schwefel_on_cube, 2), 1, "rough", 24),
        ("morton_rastrigin_d2", morton_1d(rastrigin_on_cube, 2), 1, "rough", 24),
        ("pool", pool, d_pool, "smooth", 24),
        ("mini_golf", mini_golf, d_golf, "smooth", 24),
        ("rosenbrock_d3", lambda x: rosenbrock_on_cube(x), 3, "smooth", 24),
    ]


METHODS = ["grass3", "golden2", "golden6", "brent", "random"]


def run_method(method, obj, n_dim, n_trials, seed):
    if method == "grass3":
        return iterated_line_search(obj, n_dim, n_trials, GrassInner(), seed)
    if method == "golden2":
        return iterated_line_search(obj, n_dim, n_trials, golden_inner(2), seed)
    if method == "golden6":
        return iterated_line_search(obj, n_dim, n_trials, golden_inner(6), seed)
    if method == "brent":
        return iterated_line_search(obj, n_dim, n_trials, brent_inner(10), seed)
    if method == "random":
        return random_search(obj, n_dim, n_trials, seed)
    raise ValueError(method)


if __name__ == "__main__":
    n_trials = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    out = {"n_trials": n_trials, "problems": {}}
    for name, obj, n_dim, family, seeds in build_problems():
        t0 = time.time()
        rows = {}
        for method in METHODS:
            vals = [run_method(method, obj, n_dim, n_trials, s)[0] for s in range(seeds)]
            rows[method] = vals
        out["problems"][name] = {"family": family, "n_dim": n_dim, "seeds": seeds, "results": rows}
        med = {m: float(np.median(v)) for m, v in rows.items()}
        order = sorted(med, key=med.get)
        print(f"{name:20s} ({family}, d={n_dim}, {time.time() - t0:5.1f}s) " + "  ".join(f"{m}={med[m]:.4g}" for m in order))
        # per-seed win counts of grass3 vs each classical inner
        for rival in ("golden2", "golden6", "brent"):
            wins = sum(g < r for g, r in zip(rows["grass3"], rows[rival]))
            ties = sum(g == r for g, r in zip(rows["grass3"], rows[rival]))
            print(f"{'':20s}   grass3 vs {rival:7s}: {wins}/{len(rows['grass3'])} wins ({ties} ties)")
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote results.json")
