"""exp2d: the dimension law, isolated. Same five methods, same outer
loop, scalable classic objectives at d = 2..32. If the high-d wins in
exp2b (wind_farm d=16, rocket d=12) are the per-line-economy effect
and not something about those simulators, the grass-vs-expensive-inner
gap should widen with d on ordinary landscapes too.
"""

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/Users/petercotton/github/humpday")

from run_bench import METHODS, run_method  # noqa: E402

from humpday.objectives.classic import (  # noqa: E402
    griewank_on_cube,
    rastrigin_on_cube,
    rosenbrock_on_cube,
    schwefel_on_cube,
)

OBJECTIVES = [
    ("rastrigin", rastrigin_on_cube),
    ("schwefel", schwefel_on_cube),
    ("rosenbrock", rosenbrock_on_cube),
    ("griewank", griewank_on_cube),
]
DIMS = [2, 4, 8, 16, 32]
SEEDS = 24

if __name__ == "__main__":
    n_trials = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    out = {"n_trials": n_trials, "seeds": SEEDS, "sweep": {}}
    for name, obj in OBJECTIVES:
        out["sweep"][name] = {}
        for d in DIMS:
            t0 = time.time()
            rows = {
                m: [run_method(m, obj, d, n_trials, s)[0] for s in range(SEEDS)]
                for m in METHODS
            }
            med = {m: float(np.median(v)) for m, v in rows.items()}
            wins_brent = sum(g < r for g, r in zip(rows["grass3"], rows["brent"]))
            wins_g6 = sum(g < r for g, r in zip(rows["grass3"], rows["golden6"]))
            out["sweep"][name][d] = {"results": rows, "medians": med}
            order = sorted(med, key=med.get)
            rank = order.index("grass3") + 1
            print(
                f"{name:11s} d={d:2d} grass rank {rank}/5  vs brent {wins_brent}/{SEEDS}"
                f"  vs golden6 {wins_g6}/{SEEDS}  ({time.time() - t0:4.1f}s)  "
                + "  ".join(f"{m}={med[m]:.4g}" for m in order),
                flush=True,
            )
    with open(os.path.join(HERE, "dimsweep_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote dimsweep_results.json")
