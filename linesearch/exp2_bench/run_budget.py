"""exp2g: budget scaling. The whole study so far sits at 120
evaluations -- the few-shot regime the 3-shot rule was born for. Does
the grass edge survive at 360 and 1080 evaluations, where precision
methods (Brent's superlinear convergence, CMA-ES's covariance
learning) have room to work? And does it strengthen at 40?

Problems: the demos where grass wins at 120 (plinko, wind_farm,
robot_arm), one needle it fixed (free_kick), one smooth control
(mini_golf), and the structured classics at d=8. CMA-ES rides along
as the external reference.
"""

import json
import os
import random
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/Users/petercotton/github/humpday")
sys.path.insert(0, "/Users/petercotton/github/humpday/example_applications")

from run_family import get_objective  # noqa: E402
from ou3_linesearch import (  # noqa: E402
    GrassInner,
    brent_inner,
    golden_inner,
    iterated_line_search,
)

from humpday.objectives.classic import (  # noqa: E402
    griewank_on_cube,
    rastrigin_on_cube,
    rosenbrock_on_cube,
)
from humpday.optimizers.alloptimizers import PURE_OPTIMIZERS  # noqa: E402

BUDGETS = [40, 120, 360, 1080]
SEEDS = 24


def problems():
    for demo in ("plinko_funnel", "wind_farm", "robot_arm", "free_kick", "mini_golf"):
        obj, d = get_objective(demo)
        yield demo, obj, d
    yield "rosenbrock_d8", lambda x: rosenbrock_on_cube(x), 8
    yield "griewank_d8", lambda x: griewank_on_cube(x), 8
    yield "rastrigin_d8", lambda x: rastrigin_on_cube(x), 8


def run(method, obj, d, n_trials, seed):
    if method == "cmaes":
        np.random.seed(seed)
        random.seed(seed)
        opt = PURE_OPTIMIZERS["CMAEvolutionStrategy"](
            lambda x: float(obj(list(x))), n_trials, d
        )
        try:
            opt.optimize()
        except Exception:
            pass
        return float(opt.best_value)
    inner = {
        "grass2U": lambda: GrassInner(skip_third=True, uniform_flee=True),
        "golden2": lambda: golden_inner(2),
        "golden6": lambda: golden_inner(6),
        "brent": lambda: brent_inner(10),
    }[method]()
    return float(iterated_line_search(obj, d, n_trials, inner, seed)[0])


METHODS = ["grass2U", "golden2", "golden6", "brent", "cmaes"]

if __name__ == "__main__":
    out = {"seeds": SEEDS, "budgets": BUDGETS, "problems": {}}
    for name, obj, d in problems():
        out["problems"][name] = {"n_dim": d}
        for n_trials in BUDGETS:
            t0 = time.time()
            rows = {
                m: [run(m, obj, d, n_trials, s) for s in range(SEEDS)] for m in METHODS
            }
            med = {m: float(np.median(v)) for m, v in rows.items()}
            out["problems"][name][n_trials] = {"results": rows, "medians": med}
            order = sorted(med, key=med.get)
            rank = order.index("grass2U") + 1
            print(
                f"{name:14s} B={n_trials:4d} grass2U rank {rank}/5  "
                + "  ".join(f"{m}={med[m]:.4g}" for m in order)
                + f"  ({time.time() - t0:5.1f}s)",
                flush=True,
            )
    with open(os.path.join(HERE, "budget_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote budget_results.json")
