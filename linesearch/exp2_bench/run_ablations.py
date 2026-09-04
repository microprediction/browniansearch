"""exp2c: mechanism ablations. Which ingredient of the grass inner
earns the high-d and rough-family wins from exp2b?

Variants, all in the shared outer loop:
  grass3      the full rule (reference)
  grass2      two-shot only: 1 eval/line, no third placement -- is the
              paper's third-shot machinery (quartic/interior) adding
              anything beyond adaptive step placement?
  grassK      kappa frozen at 20 -- does online scale adaptation matter?
  grassU      flee lands uniformly on the far half of the segment
              instead of its end -- removes the cube-boundary bias
              diagnosed on free_kick (73/102 lines fled to an endpoint)
  es5         fixed-step (1+1) descent, one eval/line at step 0.05 with
              random sign -- the naive rival: is the OU machinery just
              an expensive way to pick a constant step size?
  golden2loc  golden2 restricted to anchor +/- 0.1 -- is golden's
              full-segment reach (not its probe geometry) what loses
              in high d?
  golden2     unrestricted golden2 (reference rival)
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

from run_family import DEMOS, eval_cost_ms, get_objective  # noqa: E402
from ou3_linesearch import (  # noqa: E402
    GrassInner,
    alpha_range,
    golden_inner,
    iterated_line_search,
)


def es_inner(step=0.05):
    """(1+1)-style fixed step: one eval per line at +/-step, keep if better."""

    def search(budget, p, fp, v, rng):
        lo, hi = alpha_range(p, v)
        a = step if rng.uniform() < 0.5 else -step
        a = float(np.clip(a, lo, hi))
        if abs(a) < 1e-9 or budget.remaining() <= 0:
            return p, fp
        f = budget(p + a * v)
        return (np.clip(p + a * v, 0, 1), f) if f < fp else (p, fp)

    return search


def golden_local(reach=0.1):
    """golden2's probe geometry on a segment restricted to anchor +/- reach."""
    invphi = (np.sqrt(5.0) - 1) / 2

    def search(budget, p, fp, v, rng):
        lo, hi = alpha_range(p, v)
        lo, hi = max(lo, -reach), min(hi, reach)
        if hi - lo < 1e-9:
            return p, fp
        best_a, best_f = 0.0, fp
        for t in (hi - invphi * (hi - lo), lo + invphi * (hi - lo)):
            if budget.remaining() <= 0:
                break
            f = budget(p + t * v)
            if f < best_f:
                best_a, best_f = t, f
        return np.clip(p + best_a * v, 0, 1), best_f

    return search


VARIANTS = {
    "grass3": lambda: GrassInner(),
    "grass2": lambda: GrassInner(skip_third=True),
    "grassK": lambda: GrassInner(adapt_kappa=False),
    "grassU": lambda: GrassInner(uniform_flee=True),
    "es5": lambda: es_inner(0.05),
    "golden2loc": lambda: golden_local(0.1),
    "golden2": lambda: golden_inner(2),
}


if __name__ == "__main__":
    n_trials = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    out = {"n_trials": n_trials, "problems": {}}
    for demo in DEMOS:
        t0 = time.time()
        obj, d = get_objective(demo)
        ms = eval_cost_ms(obj, d)
        seeds = 24 if ms < 2 else (16 if ms < 30 else 8)
        rows = {}
        for name, make in VARIANTS.items():
            rows[name] = [
                iterated_line_search(obj, d, n_trials, make(), s)[0]
                for s in range(seeds)
            ]
        med = {m: float(np.median(v)) for m, v in rows.items()}
        out["problems"][demo] = {
            "n_dim": d,
            "seeds": seeds,
            "results": rows,
            "medians": med,
        }
        order = sorted(med, key=med.get)
        print(
            f"{demo:22s} d={d:2d} ({time.time() - t0:5.1f}s) "
            + "  ".join(f"{m}={med[m]:.4g}" for m in order),
            flush=True,
        )
    with open(os.path.join(HERE, "ablation_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote ablation_results.json")
