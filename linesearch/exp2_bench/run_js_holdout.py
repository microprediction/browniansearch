"""exp2m: the faithful holdout sweep for Peter's basin hypothesis.

Every docs/applications page that serves objective(u) headlessly and
deterministically becomes a holdout problem. For each we emit, to
js_holdout/<demo>.json:
  - raw slice values (random-line slices, exp1 geometry) so the grass
    session applies its exp3 basin proxy IDENTICALLY to discovery and
    holdout -- no precomputed basin numbers of ours in the analysis;
  - the full benchmark rows (per-seed best values, six methods,
    budget 120) from which rank / win-loss follows under whatever
    definition matches the discovery set.
Dimensions come from the corresponding Python port's N_DIM (the JS
decode(u) length matches the port; a probe evaluation verifies the
page accepts that dimension). Pages that fail to load, hang, or are
nondeterministic are listed in js_holdout/_sweep_summary.json with
the reason.
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

from js_demo_objective import APPS, JsObjective  # noqa: E402
from ou3_linesearch import (  # noqa: E402
    GrassInner,
    brent_inner,
    golden_inner,
    iterated_line_search,
    random_search,
)

OUT = os.path.join(HERE, "js_holdout")
os.makedirs(OUT, exist_ok=True)

# JS page stem -> python package (where the stem itself is not the name)
ALIAS = {
    "boids": "boids_flocking",
    "creature": "walking_creature",
    "cart-pole": "cart_pole_policy",
    "chess": "chess_piece_values",
    "espresso": "espresso_dialin",
    "fm-synth": "fm_sound_match",
    "lens": "lens_design",
    "packing": "circle_packing",
    "plinko": "plinko_funnel",
    "punt-the-wire": "goalkeeper_punt",
    "reactor-tprofile": "reactor_profile",
    "tetris": "tetris_weights",
    "antenna": "antenna_array",
    "ebola": "ebola_response",
}
SKIP = {"index", "no-free-lunch"}

METHODS = ["grass2U", "grassEI", "golden2", "golden6", "brent", "random"]


def python_dim(stem):
    pkg = ALIAS.get(stem, stem.replace("-", "_"))
    mod = importlib.import_module(f"{pkg}.problem")
    return int(mod.N_DIM)


def slices(obj, d, n_slices, npts, seed=5):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n_slices):
        x0 = rng.uniform(0.15, 0.85, d)
        v = rng.normal(size=d)
        v /= np.linalg.norm(v)
        ts = np.linspace(-0.3, 0.3, npts)
        pts = np.clip(x0[None, :] + ts[:, None] * v[None, :], 0, 1)
        out.append([float(obj(list(p))) for p in pts])
    return out


def run(method, obj, d, seed, n_trials=120):
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
        return float(random_search(obj, d, n_trials, seed)[0])
    return float(iterated_line_search(obj, d, n_trials, makers[method](), seed)[0])


if __name__ == "__main__":
    pages = sorted(
        f[:-5] for f in os.listdir(APPS) if f.endswith(".html") and f[:-5] not in SKIP
    )
    summary = {}
    for stem in pages:
        t0 = time.time()
        name = stem.replace("-", "_") + "_js"
        try:
            d = python_dim(stem)
        except Exception as e:
            summary[stem] = f"no python dim: {str(e)[:60]}"
            print(f"{name:26s} SKIP ({summary[stem]})", flush=True)
            continue
        try:
            obj = JsObjective(stem + ".html", n_dim=d)
        except Exception as e:
            summary[stem] = f"server: {str(e)[:80]}"
            print(f"{name:26s} SKIP ({summary[stem]})", flush=True)
            continue
        try:
            rng = np.random.default_rng(0)
            u = list(rng.uniform(0.2, 0.8, d))
            v1, v2 = obj(u), obj(u)
            if not np.isfinite(v1) or v1 != v2:
                summary[stem] = f"nondeterministic or nonfinite ({v1} vs {v2})"
                print(f"{name:26s} SKIP ({summary[stem]})", flush=True)
                obj.close()
                continue
            t1 = time.time()
            n_probe = 20
            for i in range(n_probe):
                obj(list(np.random.default_rng(i).uniform(0.1, 0.9, d)))
            ms = (time.time() - t1) / n_probe * 1000
            seeds = 24 if ms < 3 else (12 if ms < 30 else 6)
            n_slices, npts = (6, 257) if ms < 30 else (4, 129)
            slice_vals = slices(obj, d, n_slices, npts)
            rows = {m: [run(m, obj, d, s) for s in range(seeds)] for m in METHODS}
            med = {m: float(np.median(v)) for m, v in rows.items()}
            order = sorted(med, key=med.get)
            rank = order.index("grass2U") + 1
            rec = {
                "demo": name,
                "html": stem + ".html",
                "n_dim": d,
                "ms_per_eval": ms,
                "seeds": seeds,
                "slice_npts": npts,
                "slice_halfwidth": 0.3,
                "slices": slice_vals,
                "results": rows,
                "medians": med,
                "grass2U_rank_of_6": rank,
            }
            with open(os.path.join(OUT, f"{name}.json"), "w") as fh:
                json.dump(rec, fh)
            summary[stem] = f"ok rank {rank}/6"
            print(
                f"{name:26s} d={d:2d} {ms:6.1f}ms rank {rank}/6 "
                + "  ".join(f"{m}={med[m]:.4g}" for m in order[:3])
                + f"  ({time.time() - t0:5.1f}s)",
                flush=True,
            )
        except Exception as e:
            summary[stem] = f"run: {str(e)[:80]}"
            print(f"{name:26s} FAIL ({summary[stem]})", flush=True)
        finally:
            obj.close()
    with open(os.path.join(OUT, "_sweep_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=2)
    ok = sum(1 for v in summary.values() if v.startswith("ok"))
    print(f"sweep done: {ok}/{len(summary)} pages usable")
