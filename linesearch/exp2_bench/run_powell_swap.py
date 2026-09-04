"""exp2i: the surgical test. Everything before this either compared
inner loops inside a custom outer loop (controlled, but not a real
optimizer) or raced whole optimizers (real, but not controlled). Here
ONLY the line search is swapped inside humpday's Powell, as shipped:
same direction-set updates, same extrapolation step, same ftol
convergence check -- Powell(Brent, stock) vs Powell(grass2U inner)
vs Powell(golden2 inner). Any difference is attributable to the line
search and nothing else.

The grass inner keeps its run-level state (standardization history,
kappa fit, stall counter) across Powell's line searches, exactly as
it does in the custom outer loop.
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
from ou3_linesearch import GrassInner, golden_inner  # noqa: E402

from humpday.optimizers.scipy_algorithms import Powell  # noqa: E402


class _BudgetShim:
    """Presents the Budget interface GrassInner expects, backed by the
    host optimizer's own evaluate() and trial budget."""

    def __init__(self, opt):
        self.opt = opt

    def remaining(self):
        return self.opt.n_trials - self.opt.evaluations

    @property
    def evaluations(self):
        return self.opt.evaluations

    def __call__(self, x):
        return float(self.opt.evaluate(np.clip(np.asarray(x, dtype=float), 0, 1)))


class SwappedPowell(Powell):
    """humpday Powell with only _linesearch_powell replaced."""

    def __init__(self, objective, n_trials, n_dim, inner=None):
        super().__init__(objective, n_trials, n_dim)
        self._inner = inner
        self._rng = np.random.default_rng(np.random.randint(2**31))
        self._shim = _BudgetShim(self)
        self._seeded_values = False

    def _linesearch_powell(self, p, xi, fval):
        if self._inner is None:
            return super()._linesearch_powell(p, xi, fval)
        xi = np.asarray([float(c) for c in xi])
        norm = float(np.linalg.norm(xi))
        if norm < 1e-12:
            return fval, p, xi
        v = xi / norm
        p_arr = np.asarray([float(c) for c in p])
        if isinstance(self._inner, GrassInner) and not self._seeded_values:
            self._inner.values.append(float(fval))
            self._seeded_values = True
        x_new, f_new = self._inner(self._shim, p_arr, float(fval), v, self._rng)
        if f_new < fval:
            return f_new, np.asarray(x_new), np.asarray(x_new) - p_arr
        return fval, p, np.zeros(len(xi))


def run(method, obj, d, n_trials, seed):
    np.random.seed(seed)
    random.seed(seed)
    wrapped = lambda x: float(obj(list(x)))  # noqa: E731
    if method == "powell_brent":
        opt = SwappedPowell(wrapped, n_trials, d, inner=None)
    elif method == "powell_grass":
        opt = SwappedPowell(
            wrapped, n_trials, d, inner=GrassInner(skip_third=True, uniform_flee=True)
        )
    elif method == "powell_golden2":
        opt = SwappedPowell(wrapped, n_trials, d, inner=golden_inner(2))
    else:
        raise ValueError(method)
    try:
        opt.optimize()
    except Exception:
        pass
    return float(opt.best_value)


METHODS = ["powell_brent", "powell_grass", "powell_golden2"]

if __name__ == "__main__":
    n_trials = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    out = {"n_trials": n_trials, "problems": {}}
    for demo in DEMOS:
        t0 = time.time()
        obj, d = get_objective(demo)
        ms = eval_cost_ms(obj, d)
        seeds = 24 if ms < 2 else (16 if ms < 30 else 8)
        rows = {m: [run(m, obj, d, n_trials, s) for s in range(seeds)] for m in METHODS}
        med = {m: float(np.median(v)) for m, v in rows.items()}
        wins = sum(g < b for g, b in zip(rows["powell_grass"], rows["powell_brent"]))
        ties = sum(g == b for g, b in zip(rows["powell_grass"], rows["powell_brent"]))
        out["problems"][demo] = {
            "n_dim": d,
            "seeds": seeds,
            "results": rows,
            "medians": med,
        }
        order = sorted(med, key=med.get)
        print(
            f"{demo:22s} d={d:2d} "
            + "  ".join(f"{m}={med[m]:.4g}" for m in order)
            + f" | grass-vs-brent {wins}/{seeds} wins ({ties} ties) ({time.time() - t0:5.1f}s)",
            flush=True,
        )
    with open(os.path.join(HERE, "powell_swap_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote powell_swap_results.json")
