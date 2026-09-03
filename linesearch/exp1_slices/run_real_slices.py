"""Slice roughness of humpday's real/physical objectives -- the
question raised by the smooth classic suite: do the real ones carry
native roughness (p toward 1 = OU) or are they smooth too?"""
import sys
import numpy as np
sys.path.insert(0, "/Users/petercotton/github/humpday")
from run_slices import variogram_p, direct_slice_p, morton_slice_p

from humpday.objectives.horse import horse_dividends_on_cube
from humpday.objectives.portfolio import (
    markowitz_analytic_on_cube, markowitz_realized_on_cube)

REAL = [("horse_dividends", horse_dividends_on_cube),
        ("markowitz_analytic", markowitz_analytic_on_cube),
        ("markowitz_realized", markowitz_realized_on_cube)]

if __name__ == "__main__":
    rng = np.random.default_rng(11)
    print("== real objectives: direct random-line slices ==")
    for d in (3, 5):
        for name, obj in REAL:
            try:
                ps = [direct_slice_p(obj, d, rng, npts=513)
                      for _ in range(8)]
                print(f"  d={d} {name:20s} median p = "
                      f"{np.nanmedian(ps):.2f}  (iqr "
                      f"{np.nanpercentile(ps,25):.2f}-"
                      f"{np.nanpercentile(ps,75):.2f})")
            except Exception as e:
                print(f"  d={d} {name}: ERROR {str(e)[:60]}")
    print("== real objectives: Morton-composed, d=2 ==")
    for name, obj in REAL:
        try:
            ps = [morton_slice_p(obj, 2, rng, npts=4097)
                  for _ in range(5)]
            print(f"  {name:20s} median p = {np.nanmedian(ps):.2f}")
        except Exception as e:
            print(f"  {name}: ERROR {str(e)[:60]}")
