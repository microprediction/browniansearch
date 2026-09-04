"""exp2f: the "so what" test. grass2U (the recommended configuration
from the ablations: two-shot rule, uniform-interior flee, 1 eval per
line) as a FULL optimizer against humpday's real catalog -- faithful
ports of CMA-ES, differential evolution, Powell, Nelder-Mead, BOBYQA,
dual annealing, Rechenberg, Alloy -- on the physics family at budget
120. Everything before this compared inner loops inside one outer
loop of my own; this is the fair external fight, everyone as shipped.
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

from run_family import DEMOS, eval_cost_ms, get_objective  # noqa: E402
from ou3_linesearch import GrassInner, golden_inner, iterated_line_search  # noqa: E402

from humpday.optimizers.alloptimizers import PURE_OPTIMIZERS  # noqa: E402

SOTA = [
    "CMAEvolutionStrategy",
    "DifferentialEvolution",
    "Powell",
    "NelderMead",
    "PRIMA_BOBYQA",
    "SimulatedAnnealing",
    "Rechenberg",
    "Alloy",
    "RandomSearch",
]


def run_humpday(name, obj, d, n_trials, seed):
    np.random.seed(seed)
    random.seed(seed)
    opt = PURE_OPTIMIZERS[name](lambda x: float(obj(list(x))), n_trials, d)
    try:
        opt.optimize()
    except Exception:
        pass  # keep best-so-far on any internal failure
    return float(opt.best_value)


def run_ours(name, obj, d, n_trials, seed):
    if name == "grass2U":
        inner = GrassInner(skip_third=True, uniform_flee=True)
    elif name == "golden2":
        inner = golden_inner(2)
    else:
        raise ValueError(name)
    return float(iterated_line_search(obj, d, n_trials, inner, seed)[0])


METHODS = ["grass2U", "golden2"] + SOTA

if __name__ == "__main__":
    n_trials = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    out = {"n_trials": n_trials, "problems": {}}
    for demo in DEMOS:
        t0 = time.time()
        obj, d = get_objective(demo)
        ms = eval_cost_ms(obj, d)
        seeds = 24 if ms < 2 else (16 if ms < 30 else 8)
        rows = {}
        for m in METHODS:
            runner = run_ours if m in ("grass2U", "golden2") else run_humpday
            rows[m] = [runner(m, obj, d, n_trials, s) for s in range(seeds)]
        med = {m: float(np.median(v)) for m, v in rows.items()}
        out["problems"][demo] = {
            "n_dim": d,
            "seeds": seeds,
            "results": rows,
            "medians": med,
        }
        order = sorted(med, key=med.get)
        rank = order.index("grass2U") + 1
        top3 = "  ".join(f"{m}={med[m]:.4g}" for m in order[:3])
        print(
            f"{demo:22s} d={d:2d} grass2U rank {rank}/{len(METHODS)} "
            f"(grass2U={med['grass2U']:.4g}) top3: {top3} ({time.time() - t0:5.1f}s)",
            flush=True,
        )
    with open(os.path.join(HERE, "vs_sota_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote vs_sota_results.json")
