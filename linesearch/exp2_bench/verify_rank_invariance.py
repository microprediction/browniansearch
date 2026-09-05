"""verify_rank_invariance: the claim behind GrassInner(standardize=
"rank") is that normal-scores standardization makes the policy depend
on observed values only through their ordering, so the search must
place IDENTICAL evaluation points on f and on g(f) for any strictly
increasing g. Linear standardization holds this only for affine g.

Two-path agreement in the sense of style/verification_conventions.md:
same computation run two ways that must agree. The linear-mode
divergence under a nonlinear warp is reported as a measurement, not a
failure -- it is the expected behavior that motivated rank mode.

One caution the test respects: the stall counter compares raw
improvements against tol = 1e-12 + 1e-9|f|, which is not order-
invariant in general. The warps used keep improvements far above tol
on this objective, so any point-sequence divergence in rank mode is a
real invariance break, not a tolerance artifact.
"""

import sys

import numpy as np

sys.path.insert(0, "/Users/petercotton/github/browniansearch/linesearch/exp2_bench")
sys.path.insert(0, "/Users/petercotton/github/humpday")

from ou3_linesearch import GrassInner, iterated_line_search  # noqa: E402

from humpday.objectives.classic import rastrigin_on_cube  # noqa: E402

D = 3
BUDGET = 60
SEEDS = range(6)

WARPS = {
    "affine": lambda v: 2.0 * v + 1.0,
    "expanding_cubic": lambda v: v + 0.1 * v**3,  # derivative 1 + 0.3 v^2 > 0
}


def eval_points(objective, seed, standardize):
    pts = []

    def wrapped(x):
        pts.append(tuple(np.round(np.asarray(x, dtype=float), 12)))
        return float(objective(list(x)))

    inner = GrassInner(skip_third=True, uniform_flee=True, standardize=standardize)
    iterated_line_search(wrapped, D, BUDGET, inner, seed)
    return pts


def first_divergence(a, b):
    for i, (p, q) in enumerate(zip(a, b)):
        if p != q:
            return i
    return None if len(a) == len(b) else min(len(a), len(b))


if __name__ == "__main__":
    base = rastrigin_on_cube
    failures = 0
    for warp_name, g in WARPS.items():

        def warped(x, g=g):
            return g(float(base(x)))

        for seed in SEEDS:
            for mode in ("rank", "linear"):
                p0 = eval_points(base, seed, mode)
                p1 = eval_points(warped, seed, mode)
                div = first_divergence(p0, p1)
                invariant = div is None
                if mode == "rank" and not invariant:
                    failures += 1
                    print(
                        f"FAIL rank mode not invariant: warp={warp_name} "
                        f"seed={seed} diverges at eval {div}"
                    )
                if mode == "linear" and warp_name == "affine" and not invariant:
                    failures += 1
                    print(
                        f"FAIL linear mode not affine-invariant: seed={seed} "
                        f"diverges at eval {div}"
                    )
                if mode == "linear" and warp_name == "expanding_cubic":
                    # measurement, not assertion: nonlinear warps SHOULD move
                    # the linear-mode trajectory
                    tag = (
                        "identical (surprising)"
                        if invariant
                        else f"diverges at eval {div}"
                    )
                    print(
                        f"  measure: linear mode under {warp_name}, seed {seed}: {tag}"
                    )
    if failures == 0:
        print(
            "PASS: rank mode point-sequences identical under all warps, "
            "all seeds; linear mode affine-invariant."
        )
    else:
        print(f"{failures} FAILURES")
        sys.exit(1)
