"""Directions per budget: how many lines each inner search lets the shared
outer loop try within 120 evaluations. Averaged over 8 seeds per problem."""
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, "/Users/petercotton/github/humpday")
sys.path.insert(0, "/Users/petercotton/github/humpday/example_applications")

from ou3_linesearch import GrassInner, brent_inner, golden_inner, iterated_line_search  # noqa: E402
from run_family import get_objective  # noqa: E402
from humpday.objectives.classic import rosenbrock_on_cube  # noqa: E402

MAKERS = {
    "grass3": lambda: GrassInner(),
    "grass2U": lambda: GrassInner(skip_third=True, uniform_flee=True),
    "golden2": lambda: golden_inner(2),
    "golden6": lambda: golden_inner(6),
    "brent": lambda: brent_inner(10),
}


def lines(obj, d, make, seed):
    inner = make()
    count = [0]

    def counted(budget, p, fp, v, rng):
        count[0] += 1
        return inner(budget, p, fp, v, rng)

    if isinstance(inner, GrassInner):
        counted = _GrassCounter(inner, count)
    iterated_line_search(obj, d, 120, counted, seed)
    return count[0]


class _GrassCounter(GrassInner):
    """Counts lines while keeping the isinstance check in the outer loop."""

    def __init__(self, inner, count):
        self.__dict__["_inner"], self.__dict__["_count"] = inner, count

    def __getattr__(self, name):
        return getattr(self._inner, name)

    def __call__(self, budget, p, fp, v, rng):
        self._count[0] += 1
        return self._inner(budget, p, fp, v, rng)


if __name__ == "__main__":
    probs = [(n, *get_objective(n)) for n in ("plinko_funnel", "wind_farm", "robot_arm", "free_kick")]
    probs += [(f"rosenbrock_d{d}", lambda x: rosenbrock_on_cube(x), d) for d in (3, 8, 32)]
    tot = {m: [] for m in MAKERS}
    for name, obj, d in probs:
        row = {m: float(np.mean([lines(obj, d, mk, s) for s in range(8)])) for m, mk in MAKERS.items()}
        for m in MAKERS:
            tot[m].append(row[m])
        print(f"{name:16s} d={d:2d} " + "  ".join(f"{m}={row[m]:5.1f}" for m in MAKERS), flush=True)
    print("mean lines per 120 evals: " + "  ".join(f"{m}={np.mean(v):5.1f}" for m, v in tot.items()))
    b = np.array(tot["brent"])
    for m in ("grass3", "grass2U"):
        r = np.array(tot[m]) / b
        print(f"{m} / brent lines: {r.min():.1f} to {r.max():.1f} (mean {r.mean():.1f})")
