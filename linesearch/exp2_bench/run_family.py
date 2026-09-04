"""exp2b: the full physics-demo family. For every humpday
example_applications demo with simulated dynamics in the objective,
measure slice roughness p (exp1 protocol) and run the same
five-method inner-line-search head-to-head (budget 120, shared outer
loop). Tests the band claim from exp2: the grass rule's edge lives at
p roughly in (0.3, 1.5) with real spatial structure, and classical
inner loops keep smooth landscapes.
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

from run_bench import METHODS, run_method  # noqa: E402
from run_slices import variogram_p  # noqa: E402

# Everything in example_applications with simulated physical dynamics
# (ballistics, collisions, rigid-body/agent sims, structural/orbital
# mechanics). Cost-tiered seed counts keep bowling tractable.
DEMOS = [
    "bowling",
    "plinko_funnel",
    "pool",
    "trebuchet",
    "mini_golf",
    "curling",
    "slingshot",
    "free_kick",
    "goalkeeper_punt",
    "darts_aim",
    "brachistochrone",
    "rocket_landing",
    "tuned_mass_damper",
    "robot_arm",
    "cart_pole_policy",
    "walking_creature",
    "boids_flocking",
    "tennis_doubles",
    "lennard_jones_cluster",
    "bridge_truss",
    "wind_farm",
    "satellite_phasing",
]


def get_objective(demo):
    mod = importlib.import_module(f"{demo}.problem")
    for name in ("objective", "simulate_throw_objective"):
        if hasattr(mod, name):
            return getattr(mod, name), mod.N_DIM
    raise AttributeError(demo)


def measure_p(obj, d, n_slices=6, npts=257, seed=5):
    """exp1 protocol: variogram exponent on random-line slices."""
    rng = np.random.default_rng(seed)
    ps = []
    for _ in range(n_slices):
        x0 = rng.uniform(0.15, 0.85, d)
        v = rng.normal(size=d)
        v /= np.linalg.norm(v)
        ts = np.linspace(-0.3, 0.3, npts)
        pts = np.clip(x0[None, :] + ts[:, None] * v[None, :], 0, 1)
        vals = np.array([float(obj(list(p))) for p in pts])
        if np.std(vals) < 1e-12:
            continue
        ps.append(variogram_p(vals, 0.6 / npts))
    return (float(np.nanmedian(ps)) if ps else float("nan")), len(ps)


def eval_cost_ms(obj, d):
    rng = np.random.default_rng(0)
    t0 = time.time()
    n = 0
    while time.time() - t0 < 0.3 and n < 40:
        obj(list(rng.uniform(0.1, 0.9, d)))
        n += 1
    return (time.time() - t0) / n * 1000


if __name__ == "__main__":
    n_trials = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    out = {"n_trials": n_trials, "problems": {}}
    for demo in DEMOS:
        t0 = time.time()
        obj, d = get_objective(demo)
        ms = eval_cost_ms(obj, d)
        seeds = 24 if ms < 2 else (16 if ms < 30 else 8)
        n_slices = 6 if ms < 30 else 4
        p_med, usable = measure_p(obj, d, n_slices=n_slices)
        rows = {}
        for method in METHODS:
            rows[method] = [
                run_method(method, obj, d, n_trials, s)[0] for s in range(seeds)
            ]
        med = {m: float(np.median(v)) for m, v in rows.items()}
        wins = {}
        for rival in ("golden2", "golden6", "brent", "random"):
            w = sum(g < r for g, r in zip(rows["grass3"], rows[rival]))
            t = sum(g == r for g, r in zip(rows["grass3"], rows[rival]))
            wins[rival] = [w, t, seeds]
        out["problems"][demo] = {
            "n_dim": d,
            "ms_per_eval": ms,
            "p": p_med,
            "p_slices": usable,
            "seeds": seeds,
            "results": rows,
            "medians": med,
            "grass_wins": wins,
        }
        order = sorted(med, key=med.get)
        rank = order.index("grass3") + 1
        winstr = " ".join(f"{r}:{w}/{n}" for r, (w, t, n) in wins.items())
        print(
            f"{demo:22s} d={d:2d} p={p_med:5.2f} grass rank {rank}/5 "
            f"| {'  '.join(f'{m}={med[m]:.4g}' for m in order)} | wins {winstr}",
            flush=True,
        )
        print(f"{'':22s} ({time.time() - t0:5.1f}s)", flush=True)
    with open(os.path.join(HERE, "family_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote family_results.json")
