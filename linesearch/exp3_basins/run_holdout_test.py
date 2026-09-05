"""Locked pre-registered test on the js_holdout sweep. No choices made
here that were not fixed in PREREGISTRATION.md."""
import glob, json, os
import numpy as np
from scipy.stats import rankdata, spearmanr

HOLD = ("/Users/petercotton/github/browniansearch/linesearch/"
        "exp2_bench/js_holdout")

# discovery-set objective stems (excluded from holdout, per prereg)
DISCOVERY = {"bowling","plinko_funnel","plinko","boids_flocking","boids",
 "tennis_doubles","tennis","free_kick","goalkeeper_punt","punt",
 "darts_aim","darts","robot_arm","rocket_landing","satellite_phasing",
 "wind_farm","cart_pole_policy","cart_pole","walking_creature","creature",
 "brachistochrone","bridge_truss","lennard_jones_cluster","tuned_mass_damper",
 "pool","curling","mini_golf","trebuchet","slingshot","punt_the_wire"}

def stem(fn):
    return os.path.basename(fn)[:-8].replace("_js","")  # strip _js.json

def basins_per_line(slices):
    per=[]
    for y in slices:
        y=np.asarray(y,float)
        if np.std(y)<1e-9: per.append(1.0); continue
        g=np.diff(y); nsc=int(np.sum(np.diff(np.sign(g))!=0))
        per.append(nsc/2+1)
    return float(np.median(per))

def grass_rank(results):
    opts=["grass2U","grassEI","golden2","golden6","brent","random"]
    med={o:np.median(results[o]) for o in opts if o in results and results[o]}
    present=list(med)
    rk=rankdata([med[o] for o in present],method="average")  # minimization
    return float(rk[present.index("grass2U")])

rows=[]; excluded=[]
for fn in sorted(glob.glob(f"{HOLD}/*.json")):
    if fn.endswith("_sweep_summary.json"): continue
    d=json.load(open(fn)); s=stem(fn)
    name=d.get("demo",s)
    key=s.replace("_js","")
    if key in DISCOVERY or name.replace("_js","") in DISCOVERY:
        excluded.append(key); continue
    if "slices" not in d or "results" not in d: 
        excluded.append(key+"(no data)"); continue
    nb=basins_per_line(d["slices"]); gr=grass_rank(d["results"])
    rows.append((key,d.get("n_dim"),nb,gr))

rows.sort(key=lambda r:r[2])
for k,dim,nb,gr in rows:
    print(f"  {k:22s} d={dim} basins/line {nb:6.1f}  grass_rank {gr:.1f}")
print(f"\nexcluded {len(excluded)} discovery-overlapping/dataless:",
      ", ".join(sorted(set(excluded))))
nb=np.array([r[2] for r in rows]); gr=np.array([r[3] for r in rows])
rho,p=spearmanr(nb,gr)
p_one = p/2 if rho>0 else 1-p/2
print(f"\nHOLDOUT n={len(rows)}")
print(f"Spearman(basins, grass_rank) = {rho:+.3f}  two-sided p={p:.4f}"
      f"  one-sided p={p_one:.4f}")
print("PRE-REGISTERED: supported iff rho>0 AND one-sided p<0.05")
verdict = "SUPPORTED" if (rho>0 and p_one<0.05) else "NOT SUPPORTED"
print("VERDICT:", verdict)
json.dump(dict(n=len(rows),rho=float(rho),p_two=float(p),
    p_one=float(p_one),verdict=verdict,
    rows=[dict(name=r[0],d=r[1],basins=r[2],rank=r[3]) for r in rows],
    excluded=sorted(set(excluded))),
    open("holdout_results.json","w"),indent=2)
