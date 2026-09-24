"""Print every line-search number quoted on the site, from the committed
result files. Usage: python3 summarize_site.py [exp2_bench dir]"""
import json
import os
import sys

import numpy as np
from scipy.stats import rankdata

HERE = os.path.dirname(os.path.abspath(__file__))
B = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "exp2_bench")


def load(name):
    with open(os.path.join(B, name)) as fh:
        return json.load(fh)


def wins(a, b):
    return sum(x < y for x, y in zip(a, b)), sum(x == y for x, y in zip(a, b)), len(a)


def tie_rank(meds, who):
    names = list(meds)
    rk = rankdata([meds[n] for n in names], method="average")
    return float(rk[names.index(who)])


# Custom outer loop, bench: plinko seed wins of the rule (grass3)
r = load("results.json")["problems"]["plinko_funnel"]["results"]
print("plinko (bench) grass3 wins vs:",
      {m: wins(r["grass3"], r[m])[:2] for m in ("golden2", "golden6", "brent")})

# Family: problems where grass3 has the best median (tie-averaged rank)
fam = load("family_results.json")["problems"]
print("family grass3 tie-averaged rank:")
for k, v in fam.items():
    meds = {m: float(np.median(x)) for m, x in v["results"].items()}
    print(f"   {k:22s} {tie_rank(meds, 'grass3'):.1f}")

# Dimension sweep: grass3 vs brent seed wins
ds = load("dimsweep_results.json")["sweep"]
for obj, byd in ds.items():
    row = []
    for d, v in byd.items():
        res = v["results"] if "results" in v else v
        row.append(f"d={d}:{wins(res['grass3'], res['brent'])[0]}")
    print(f"dimsweep {obj:10s} grass3 vs brent", " ".join(row))

# Directions: lines per run are not stored; see lines_per_budget.py

# Against engineered optimizers: mean tie-averaged rank of 11
vs = load("vs_sota_results.json")["problems"]
ranks = {}
for k, v in vs.items():
    meds = {m: float(np.median(x)) for m, x in v["results"].items()}
    for m in meds:
        ranks.setdefault(m, []).append(tie_rank(meds, m))
order = sorted(ranks, key=lambda m: np.mean(ranks[m]))
print("vs_sota mean tie-averaged rank:",
      ", ".join(f"{m} {np.mean(ranks[m]):.2f}" for m in order))
g = {k: float(np.median(v["results"]["grass2U"])) for k, v in vs.items()}
f3 = {k: float(np.median(v["results"]["grass3"])) for k, v in fam.items()}
print("grass2U (vs_sota) better median than grass3 (family) on",
      sum(g[k] < f3[k] for k in g), "of", len(g))

# Budget scaling: mean tie-averaged rank over problems per budget
bud = load("budget_results.json")
for bb in bud["budgets"]:
    rr = {}
    for k, v in bud["problems"].items():
        res = v[str(bb)]["results"] if "results" in v[str(bb)] else v[str(bb)]
        meds = {m: float(np.median(x)) for m, x in res.items()}
        for m in meds:
            rr.setdefault(m, []).append(tie_rank(meds, m))
    print(f"budget {bb:5d}: " + ", ".join(f"{m} {np.mean(x):.2f}" for m, x in
                                         sorted(rr.items(), key=lambda t: np.mean(t[1]))))

# One-step EI: grass2U vs grassEI paired seeds, and medians won
ei = load("ei_results.json")["problems"]
w2 = we = t = med2 = 0
for k, v in ei.items():
    a, b = v["results"]["grass2U"], v["results"]["grassEI"]
    w2 += sum(x < y for x, y in zip(a, b)); we += sum(y < x for x, y in zip(a, b))
    t += sum(x == y for x, y in zip(a, b)); med2 += np.median(a) < np.median(b)
print(f"EI race over {len(ei)} problems: grass2U {w2}, grassEI {we}, ties {t};"
      f" grass2U better median on {med2}")

# Own model (expOU): winner per case
ex = load("expou_results.json")["cases"]
for k, v in ex.items():
    meds = {m: float(np.median(x)) for m, x in v["results"].items()}
    best = min(meds, key=meds.get)
    print(f"expOU {k:10s} best {best:8s} grass2U tie-rank {tie_rank(meds, 'grass2U'):.1f}/6")
