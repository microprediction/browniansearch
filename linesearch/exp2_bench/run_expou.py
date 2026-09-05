"""exp2l: the home-turf control (Peter: "see how it goes on actual
high dim exp(OU)"). The objective is the model's exact native
landscape: X a Gaussian field on [0,1]^d with isotropic exponential
covariance exp(-kappa ||s - t||) -- Ornstein-Uhlenbeck along EVERY
line through the cube, p = 1 by construction -- and f = -exp(X)
minimized. Sampled lazily and exactly: each new query is drawn from
the conditional distribution given all previous queries, so the
field is a consistent random function in any dimension. (Each
method sees its own realization per seed since draws depend on query
order; comparisons are statistical over seeds, as is standard for
random-function benchmarks.)

If the grass family does not win here, nothing else in the study
matters; and the grass2U-vs-grassEI ordering at p = 1 calibrates the
acquisition-flip law seen at exp2k (table above p~0.3, EI below).
"""

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from ou3_linesearch import (  # noqa: E402
    GrassInner,
    brent_inner,
    golden_inner,
    iterated_line_search,
    random_search,
)


class LazyExpOU:
    """f(x) = -exp(X(x)), X ~ GP(0, exp(-kappa r)), sampled exactly on
    demand by sequential conditioning."""

    def __init__(self, d, kappa, seed):
        self.d = d
        self.kappa = kappa
        self.rng = np.random.default_rng(seed)
        self.pts = np.zeros((0, d))
        self.vals = np.zeros(0)

    def __call__(self, u):
        x = np.clip(np.asarray(u, dtype=float), 0.0, 1.0)
        n = len(self.vals)
        if n == 0:
            m, v = 0.0, 1.0
        else:
            dists = np.linalg.norm(self.pts - x[None, :], axis=1)
            j = int(np.argmin(dists))
            if dists[j] < 1e-12:
                return float(-np.exp(self.vals[j]))
            K = np.exp(
                -self.kappa
                * np.linalg.norm(self.pts[:, None, :] - self.pts[None, :, :], axis=2)
            )
            K[np.diag_indices_from(K)] += 1e-10
            k = np.exp(-self.kappa * dists)
            sol = np.linalg.solve(K, k)
            m = float(sol @ self.vals)
            v = max(float(1.0 - sol @ k), 1e-12)
        y = m + np.sqrt(v) * self.rng.standard_normal()
        self.pts = np.vstack([self.pts, x[None, :]])
        self.vals = np.append(self.vals, y)
        return float(-np.exp(y))


CASES = [(4, 10.0), (16, 10.0), (64, 10.0), (16, 3.0), (16, 30.0)]
SEEDS = 24
N_TRIALS = 120
METHODS = ["grass2U", "grassEI", "golden2", "golden6", "brent", "random"]


def run(method, d, kappa, seed):
    obj = LazyExpOU(d, kappa, 1000 * seed + d)
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


if __name__ == "__main__":
    out = {"n_trials": N_TRIALS, "seeds": SEEDS, "cases": {}}
    for d, kappa in CASES:
        t0 = time.time()
        rows = {m: [run(m, d, kappa, s) for s in range(SEEDS)] for m in METHODS}
        med = {m: float(np.median(v)) for m, v in rows.items()}
        wins = {
            r: sum(g < x for g, x in zip(rows["grass2U"], rows[r]))
            for r in ("grassEI", "golden2", "golden6", "brent", "random")
        }
        key = f"d{d}_k{int(kappa)}"
        out["cases"][key] = {
            "d": d,
            "kappa": kappa,
            "results": rows,
            "medians": med,
            "grass2U_wins": wins,
        }
        order = sorted(med, key=med.get)
        rank = order.index("grass2U") + 1
        print(
            f"expOU d={d:2d} kappa={kappa:4.0f} grass2U rank {rank}/6  "
            + "  ".join(f"{m}={med[m]:.4g}" for m in order)
            + f" | wins {wins} ({time.time() - t0:5.1f}s)",
            flush=True,
        )
    with open(os.path.join(HERE, "expou_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote expou_results.json")
