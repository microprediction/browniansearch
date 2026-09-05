"""exp2k: the full-fidelity JS demos as benchmark objectives. The
Python ports of pool/trebuchet/mini_golf/curling/slingshot are
reduced-order stand-ins (and measured smooth, p=1.6-2.0, landing them
in golden/Brent territory in exp2b). The JS originals run the real
Matter.js multi-body physics. Question: are the TRUE landscapes rough
-- collision-cascade territory -- and does the grass family win there?
"""

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "exp1_slices"))

from js_demo_objective import JS_DEMOS, JsObjective  # noqa: E402
from run_slices import variogram_p  # noqa: E402
from ou3_linesearch import (  # noqa: E402
    GrassInner,
    brent_inner,
    golden_inner,
    iterated_line_search,
    random_search,
)

SEEDS = 24
N_TRIALS = 120


def measure_p(obj, d, n_slices=6, npts=257, seed=5):
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


def run(method, obj, d, seed):
    makers = {
        "grass2U": lambda: GrassInner(skip_third=True, uniform_flee=True),
        "grassEI": lambda: GrassInner(
            placement="ei", skip_third=True, uniform_flee=True
        ),
        "golden2": lambda: golden_inner(2),
        "golden6": lambda: golden_inner(6),
        "brent": lambda: brent_inner(10),
    }
    if method == "random":
        return float(random_search(obj, d, N_TRIALS, seed)[0])
    return float(iterated_line_search(obj, d, N_TRIALS, makers[method](), seed)[0])


METHODS = ["grass2U", "grassEI", "golden2", "golden6", "brent", "random"]

if __name__ == "__main__":
    out = {"n_trials": N_TRIALS, "seeds": SEEDS, "problems": {}}
    for demo in JS_DEMOS:
        t0 = time.time()
        obj = JsObjective(demo)
        d = obj.n_dim
        p_med, usable = measure_p(obj, d)
        rows = {m: [run(m, obj, d, s) for s in range(SEEDS)] for m in METHODS}
        obj.close()
        med = {m: float(np.median(v)) for m, v in rows.items()}
        wins = {
            r: sum(g < x for g, x in zip(rows["grass2U"], rows[r]))
            for r in ("golden2", "golden6", "brent", "random")
        }
        out["problems"][demo] = {
            "n_dim": d,
            "p": p_med,
            "p_slices": usable,
            "results": rows,
            "medians": med,
            "grass2U_wins": wins,
        }
        order = sorted(med, key=med.get)
        rank = order.index("grass2U") + 1
        print(
            f"{demo:14s} d={d} p={p_med:5.2f} grass2U rank {rank}/6 "
            + "  ".join(f"{m}={med[m]:.4g}" for m in order)
            + f" | wins {wins} ({time.time() - t0:5.1f}s)",
            flush=True,
        )
    with open(os.path.join(HERE, "js_family_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote js_family_results.json")
