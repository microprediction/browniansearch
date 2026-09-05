"""exp2j: the acquisition swap (Peter's waste-a-call point made
formal). The paper's rule optimizes TERMINAL placement -- you live at
your final point, so "stay" is real. An optimizer keeps the running
best, so an unspent call is worth nothing and the true question per
call is local-model-probe vs global fresh draw. The matched
acquisition is expected improvement over the incumbent, i.e. 1-D
Bayesian optimization on the OU line with kappa learned online, and
rho = 0 (the fresh draw) as the standing rival inside the same
maximization -- dlib's MaxLIPO+TR local/global alternation with a
probabilistic bound instead of a Lipschitz one.

grassEI = EI placement + uniform flee + no third shot. Raced against
grass2U (the terminal-payoff table), golden2, and random on the rough
family, the high-d wins, the fixed needle, and classics at d=16/32.
"""

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/Users/petercotton/github/humpday")
sys.path.insert(0, "/Users/petercotton/github/humpday/example_applications")

from run_family import eval_cost_ms, get_objective  # noqa: E402
from ou3_linesearch import (  # noqa: E402
    GrassInner,
    golden_inner,
    iterated_line_search,
    random_search,
)

from humpday.objectives.classic import (  # noqa: E402
    griewank_on_cube,
    rastrigin_on_cube,
    rosenbrock_on_cube,
)

DEMOS = [
    "bowling",
    "plinko_funnel",
    "boids_flocking",
    "tennis_doubles",
    "wind_farm",
    "robot_arm",
    "rocket_landing",
    "free_kick",
    "tuned_mass_damper",
    "mini_golf",
]


def problems():
    for demo in DEMOS:
        obj, d = get_objective(demo)
        yield demo, obj, d
    yield "rosenbrock_d16", lambda x: rosenbrock_on_cube(x), 16
    yield "griewank_d16", lambda x: griewank_on_cube(x), 16
    yield "rastrigin_d16", lambda x: rastrigin_on_cube(x), 16
    yield "griewank_d32", lambda x: griewank_on_cube(x), 32


def run(method, obj, d, n_trials, seed):
    makers = {
        "grassEI": lambda: GrassInner(
            placement="ei", skip_third=True, uniform_flee=True
        ),
        "grass2U": lambda: GrassInner(skip_third=True, uniform_flee=True),
        "golden2": lambda: golden_inner(2),
    }
    if method == "random":
        return float(random_search(obj, d, n_trials, seed)[0])
    return float(iterated_line_search(obj, d, n_trials, makers[method](), seed)[0])


METHODS = ["grassEI", "grass2U", "golden2", "random"]

if __name__ == "__main__":
    n_trials = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    out = {"n_trials": n_trials, "problems": {}}
    for name, obj, d in problems():
        t0 = time.time()
        ms = eval_cost_ms(obj, d)
        seeds = 24 if ms < 2 else (16 if ms < 30 else 8)
        rows = {m: [run(m, obj, d, n_trials, s) for s in range(seeds)] for m in METHODS}
        med = {m: float(np.median(v)) for m, v in rows.items()}
        wins2u = sum(a < c for a, c in zip(rows["grassEI"], rows["grass2U"]))
        ties2u = sum(a == c for a, c in zip(rows["grassEI"], rows["grass2U"]))
        wg = sum(a < c for a, c in zip(rows["grassEI"], rows["golden2"]))
        out["problems"][name] = {
            "n_dim": d,
            "seeds": seeds,
            "results": rows,
            "medians": med,
        }
        order = sorted(med, key=med.get)
        print(
            f"{name:16s} d={d:2d} "
            + "  ".join(f"{m}={med[m]:.4g}" for m in order)
            + f" | EI-vs-2U {wins2u}/{seeds} ({ties2u} ties), EI-vs-golden2 {wg}/{seeds}"
            + f" ({time.time() - t0:5.1f}s)",
            flush=True,
        )
    with open(os.path.join(HERE, "ei_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote ei_results.json")
