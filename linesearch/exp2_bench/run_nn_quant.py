"""exp2e: two candidate application domains beyond the physics demos
(Peter's suggestions): neural-network weight fitting and post-training
quantization, both as derivative-free problems on the cube.

NN WEIGHTS (teacher-student): fit a tanh MLP's weights by DFO. Cube
maps to weights in [-3, 3]; objective is MSE against a fixed random
teacher of the same architecture on a fixed input batch. This is the
high-d smooth-ish regime (d = 33 and 65 here) -- the exp2b dimension
hypothesis predicts a grass edge from per-line economy.

QUANTIZATION: train a small MLP properly (numpy backprop, sine
regression), then choose PER-CHANNEL weight-quantization scale
multipliers (log-space in [1/4, 4]) at 3 bits to minimize post-quant
loss. round() makes the landscape a staircase -- genuinely rough but
spatially structured, the navigable-rough regime, at moderate-high d
(one scale per hidden unit + output scale: d = 17).
"""

import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from run_bench import METHODS, run_method  # noqa: E402

SEEDS = 24


# ---------------------------------------------------------------------------
# NN weight fitting (teacher-student)
# ---------------------------------------------------------------------------


def mlp_forward(x, w1, b1, w2, b2):
    return np.tanh(x @ w1 + b1) @ w2 + b2


def make_nn_objective(n_in=2, n_hidden=8, seed=0):
    rng = np.random.default_rng(seed)
    tw1 = rng.normal(0, 1.0, (n_in, n_hidden))
    tb1 = rng.normal(0, 0.5, n_hidden)
    tw2 = rng.normal(0, 1.0, (n_hidden, 1))
    tb2 = rng.normal(0, 0.5, 1)
    X = rng.uniform(-2, 2, (256, n_in))
    y = mlp_forward(X, tw1, tb1, tw2, tb2)
    d = n_in * n_hidden + n_hidden + n_hidden + 1

    def objective(u):
        w = (np.asarray(u, dtype=float) - 0.5) * 6.0  # [0,1] -> [-3,3]
        i = 0
        w1 = w[i : i + n_in * n_hidden].reshape(n_in, n_hidden)
        i += n_in * n_hidden
        b1 = w[i : i + n_hidden]
        i += n_hidden
        w2 = w[i : i + n_hidden].reshape(n_hidden, 1)
        i += n_hidden
        b2 = w[i : i + 1]
        return float(np.mean((mlp_forward(X, w1, b1, w2, b2) - y) ** 2))

    return objective, d


# ---------------------------------------------------------------------------
# Post-training quantization (per-channel scales)
# ---------------------------------------------------------------------------


def train_sine_mlp(n_hidden=16, seed=0, steps=4000, lr=0.02):
    """Plain numpy backprop: y = sin(3x) + 0.5 sin(7x) regression."""
    rng = np.random.default_rng(seed)
    X = rng.uniform(-1, 1, (512, 1))
    y = np.sin(3 * X) + 0.5 * np.sin(7 * X)
    w1 = rng.normal(0, 1.0, (1, n_hidden))
    b1 = np.zeros(n_hidden)
    w2 = rng.normal(0, 0.5, (n_hidden, 1))
    b2 = np.zeros(1)
    for _ in range(steps):
        h = np.tanh(X @ w1 + b1)
        pred = h @ w2 + b2
        err = pred - y  # (n,1)
        gw2 = h.T @ err / len(X)
        gb2 = err.mean(0)
        dh = (err @ w2.T) * (1 - h * h)
        gw1 = X.T @ dh / len(X)
        gb1 = dh.mean(0)
        w1 -= lr * gw1
        b1 -= lr * gb1
        w2 -= lr * gw2
        b2 -= lr * gb2
    return (X, y), (w1, b1, w2, b2)


def quantize(w, scale, bits=3):
    q = np.clip(np.round(w / scale), -(2 ** (bits - 1)), 2 ** (bits - 1) - 1)
    return q * scale


def make_quant_objective(bits=3, seed=0):
    (X, y), (w1, b1, w2, b2) = train_sine_mlp(seed=seed)
    n_hidden = w1.shape[1]
    base1 = np.abs(w1).max(axis=0) / (2 ** (bits - 1))  # per-channel base
    base2 = np.abs(w2).max() / (2 ** (bits - 1))
    d = n_hidden + 1

    def objective(u):
        u = np.asarray(u, dtype=float)
        mult = 4.0 ** (2.0 * u - 1.0)  # [0,1] -> [1/4, 4] log-space
        s1 = np.maximum(base1 * mult[:n_hidden], 1e-9)
        s2 = max(base2 * mult[n_hidden], 1e-9)
        qw1 = quantize(w1, s1[None, :], bits)
        qw2 = quantize(w2, s2, bits)
        pred = np.tanh(X @ qw1 + b1) @ qw2 + b2
        return float(np.mean((pred - y) ** 2))

    return objective, d


PROBLEMS = [
    ("nn_teacher_d33", lambda: make_nn_objective(2, 8, seed=0)),
    ("nn_teacher_d65", lambda: make_nn_objective(4, 12, seed=0)),
    ("quant_3bit_d17", lambda: make_quant_objective(bits=3, seed=0)),
    ("quant_4bit_d17", lambda: make_quant_objective(bits=4, seed=0)),
]


if __name__ == "__main__":
    n_trials = int(sys.argv[1]) if len(sys.argv) > 1 else 120
    out = {"n_trials": n_trials, "seeds": SEEDS, "problems": {}}
    for name, make in PROBLEMS:
        t0 = time.time()
        obj, d = make()
        rows = {
            m: [run_method(m, obj, d, n_trials, s)[0] for s in range(SEEDS)]
            for m in METHODS
        }
        med = {m: float(np.median(v)) for m, v in rows.items()}
        wins = {
            r: sum(g < x for g, x in zip(rows["grass3"], rows[r]))
            for r in ("golden2", "golden6", "brent", "random")
        }
        out["problems"][name] = {
            "n_dim": d,
            "results": rows,
            "medians": med,
            "grass_wins": wins,
        }
        order = sorted(med, key=med.get)
        rank = order.index("grass3") + 1
        print(
            f"{name:16s} d={d:2d} grass rank {rank}/5 ({time.time() - t0:4.1f}s) "
            + "  ".join(f"{m}={med[m]:.4g}" for m in order)
            + f" | wins {wins}",
            flush=True,
        )
    with open(os.path.join(HERE, "nn_quant_results.json"), "w") as fh:
        json.dump(out, fh, indent=2)
    print("wrote nn_quant_results.json")
