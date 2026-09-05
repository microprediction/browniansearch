"""Test the budget-vs-basins hypothesis on the discovery set."""
import importlib, json, sys
import numpy as np
from scipy.stats import rankdata, spearmanr
sys.path.insert(0, "/Users/petercotton/github/humpday")
sys.path.insert(0, "/Users/petercotton/github/humpday/example_applications")

OBJ = {'bowling':'objective','plinko_funnel':'objective','pool':'objective',
 'trebuchet':'throw_range','mini_golf':'finish_distance','curling':'stop_distance',
 'boids_flocking':'objective','tennis_doubles':'objective','slingshot':'objective',
 'free_kick':'objective','goalkeeper_punt':'objective','darts_aim':'objective',
 'robot_arm':'objective','rocket_landing':'objective','satellite_phasing':'objective',
 'wind_farm':'objective','cart_pole_policy':'objective','walking_creature':'objective',
 'brachistochrone':'objective','bridge_truss':'objective',
 'lennard_jones_cluster':'objective','tuned_mass_damper':'objective'}

def getobj(name):
    m=importlib.import_module(f"{name}.problem")
    for cand in (OBJ.get(name),'objective','throw_range','finish_distance','stop_distance','loss'):
        if cand and hasattr(m,cand): return getattr(m,cand), m.N_DIM
    raise AttributeError(name)

def basins(obj, d, n_slice=20, npts=200, rng=None):
    counts=[]
    for _ in range(n_slice):
        x0=rng.uniform(0.1,0.9,d); u=rng.normal(size=d); u/=np.linalg.norm(u)
        ts=np.linspace(-0.4,0.4,npts)
        pts=np.clip(x0[None,:]+ts[:,None]*u[None,:],0,1)
        y=np.array([float(obj(list(p))) for p in pts])
        if np.std(y)<1e-9: counts.append(1.0); continue
        g=np.diff(y); counts.append(np.sum(np.diff(np.sign(g))!=0)/2 + 1)
    return float(np.median(counts))

if __name__=="__main__":
    rng=np.random.default_rng(4)
    v=json.load(open("/Users/petercotton/github/browniansearch/linesearch/exp2_bench/vs_sota_results.json"))
    probs=v['problems']; rows=[]
    for name in sorted(OBJ):
        try:
            obj,d=getobj(name); nb=basins(obj,d,rng=rng)
            med=probs[name]['medians']; present=[o for o in med if med[o] is not None]
            vals=np.array([med[o] for o in present]); rk=rankdata(vals,method='average')
            gr=float(rk[present.index('grass2U')]); rows.append((name,d,nb,gr))
            print(f"  {name:20s} d={d:2d} basins/line {nb:5.1f}  grass_rank {gr:.1f}")
        except Exception as e:
            print(f"  {name:20s} SKIP {str(e)[:50]}")
    nb=np.array([r[2] for r in rows]); gr=np.array([r[3] for r in rows])
    rho,p=spearmanr(nb,gr)
    print(f"\nSpearman(basins/line, grass_rank) = {rho:+.3f}  p={p:.3f}  (n={len(rows)})")
    print("positive rho => more basins, worse rank => hypothesis SUPPORTED")
    json.dump([{'name':r[0],'d':r[1],'basins':r[2],'rank':r[3]} for r in rows], open("basins_results.json","w"),indent=2)
