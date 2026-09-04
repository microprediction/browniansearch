"""The trace-split three-shot replay on the Feng WiFi floor.

Setup per held-out trace (a contiguous same-row run of 15+ grid
points for one AP): the detrended log-power residual r(s) plus the
fitted AP trend is the latent payoff surface, known densely from the
120-sample means. The searcher sees the value at an incumbent grid
point, places ONE more measurement anywhere on the trace, then
commits to a deployment point on the trace; the score is the true
surface value at the deployment.

Model fitted on TRAINING traces only (split by whole traces):
residual variance s2, exponential correlation with length L (grid
units), nugget share -- the OU component the policies reason with.

Policies compared (all see the same incumbent, same model):
  incumbent    deploy the incumbent point, no experiment
  twoshot      place the experiment at the OU-optimal two-shot step
               from the incumbent (paper's rule), deploy better of
               the two observed points (no interior placement)
  equispaced   experiment at the far end of the trace, deploy best
               observed
  threeshot    the paper's full rule: experiment as in twoshot, then
               deploy the posterior-optimal point anywhere on the
               trace (interior, exterior, or observed), maximizing
               conditional mean + variance/2 of the OU component
  kg           experiment at the empirical knowledge-gradient point
               (grid search: for each candidate, Gauss-Hermite over
               its predicted value of the post-observation deploy
               optimum), then deploy as threeshot
Scoring: true detrended surface value at the deployed point,
averaged over held-out traces and incumbent choices.
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import skew, kurtosis

BASE = ("/private/tmp/claude-501/-Users-petercotton-github-winning/"
        "4cfe1164-1ade-46c7-a29a-33bedf35fe90/scratchpad/wifi_feng/"
        "WiFi-RTT-RSS-dataset-main/dataset/")

def build_traces():
    df = pd.concat([pd.read_csv(BASE + f, sep="\t", low_memory=False)
                    for f in ("dataset_building_floor_train.csv",
                              "dataset_building_floor_test.csv")],
                   ignore_index=True)
    rss_cols = [c for c in df.columns if "RSS" in c]
    recs = []
    for (x, y), g in df.groupby(["X", "Y"]):
        for ai, c in enumerate(rss_cols):
            r = g[c].values.astype(float)
            det = r > -150
            if det.sum() >= 30:
                recs.append((x, y, ai,
                             np.log(np.mean(10 ** (r[det] / 10)))))
    obs = pd.DataFrame(recs, columns=["x", "y", "ap", "X"])
    obs["resid"] = np.nan
    for ai, g in obs.groupby("ap"):
        s = g[["x", "y"]].values.astype(float)
        Xv = g["X"].values
        i0 = np.argmax(Xv)
        def nll(p):
            x0, y0, A, cc = p
            dd = np.sqrt((s[:, 0] - x0) ** 2 + (s[:, 1] - y0) ** 2
                         + 0.25)
            return np.sum((Xv - A + cc * np.log(dd)) ** 2)
        best = None
        for init in ([s[i0, 0], s[i0, 1], Xv.max(), 2.0],
                     [s[:, 0].mean(), s[:, 1].mean(), Xv.mean(), 2.0]):
            rr = minimize(nll, init, method="Nelder-Mead",
                          options=dict(maxiter=4000))
            if best is None or rr.fun < best.fun:
                best = rr
        x0, y0, A, cc = best.x
        dd = np.sqrt((s[:, 0] - x0) ** 2 + (s[:, 1] - y0) ** 2 + 0.25)
        obs.loc[g.index, "resid"] = Xv - (A - cc * np.log(dd))
    traces = []
    for (ai, y), g in obs.groupby(["ap", "y"]):
        g = g.sort_values("x")
        xs = g["x"].values; rs = g["resid"].values
        run = [0]
        for i, st in enumerate(np.round(np.diff(xs)).astype(int)):
            if st == 1:
                run.append(i + 1)
            else:
                if len(run) >= 15:
                    traces.append(rs[run])
                run = [i + 1]
        if len(run) >= 15:
            traces.append(rs[run])
    return traces

def fit_model(train):
    allv = np.concatenate(train)
    s2 = float(np.var(allv))
    lags = np.arange(1, 11)
    corr = []
    for h in lags:
        a = np.concatenate([t[:-h] for t in train if len(t) > h])
        b = np.concatenate([t[h:] for t in train if len(t) > h])
        corr.append(np.corrcoef(a, b)[0, 1])
    corr = np.array(corr)
    coef = np.polyfit(lags, np.log(np.maximum(corr, 1e-3)), 1)
    L = -1 / coef[0]; amp = np.exp(coef[1])
    return dict(s2=s2, L=L, amp=amp, mean=float(np.mean(allv)),
                s2_ou=amp * s2, s2_nug=(1 - amp) * s2)

def posterior(model, pts, vals, grid):
    """OU-component posterior mean/var at grid points, observing
    surface values (which include the nugget) at pts."""
    L, s2o, s2n = model["L"], model["s2_ou"], model["s2_nug"]
    K = s2o * np.exp(-np.abs(np.subtract.outer(pts, pts)) / L) \
        + (s2n + 1e-9) * np.eye(len(pts))
    ks = s2o * np.exp(-np.abs(np.subtract.outer(grid, pts)) / L)
    sol = np.linalg.solve(K, np.asarray(vals))
    mu = ks @ sol
    var = s2o - np.einsum("ij,ji->i", ks,
                          np.linalg.solve(K, ks.T))
    return mu, np.maximum(var, 0)

def deploy_best(model, pts, vals, n):
    grid = np.arange(n, dtype=float)
    mm = model["mean"]
    mu, var = posterior(model, np.asarray(pts),
                        np.asarray(vals) - mm, grid)
    crit = mu + mm + (var + model["s2_nug"]) / 2
    # deploying at an observed point pays its known value exactly
    j = int(np.argmax(crit))
    best_obs = int(np.argmax(vals))
    if vals[best_obs] >= crit[j]:
        return int(pts[best_obs])
    return j

def run_replay(traces, seed=0, n_inc=5):
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(traces))
    ntr = len(traces) // 2
    train = [traces[i] for i in order[:ntr]]
    test = [traces[i] for i in order[ntr:]]
    model = fit_model(train)
    print(f"model: var {model['s2']:.3f}, L {model['L']:.2f}, "
          f"OU share {model['amp']:.2f}")
    scores = {k: [] for k in ("incumbent", "twoshot", "equispaced",
                              "threeshot", "kg")}
    zq, wq = np.polynomial.hermite_e.hermegauss(15)
    wq = wq / wq.sum()
    for t in test:
        n = len(t)
        for _ in range(n_inc):
            i0 = int(rng.integers(2, n - 2))
            v0 = t[i0]
            scores["incumbent"].append(t[i0])
            # two-shot OU step: correlation lam* = clip of v0-based
            # rule needs standardized value; b = v0/sd_ou
            sdo = np.sqrt(model["s2_ou"])
            b = (v0 - model["mean"]) / sdo
            lam = min(max(b, 0.0), 1.0)
            step = max(1, int(round(-model["L"] * np.log(max(lam,
                       1e-6)))) if lam > 0 else n)
            i1 = i0 + step if i0 + step < n else max(0, i0 - step)
            i1 = int(np.clip(i1, 0, n - 1))
            v1 = t[i1]
            scores["twoshot"].append(max(v0, v1))
            ie = n - 1 if i0 < n / 2 else 0
            scores["equispaced"].append(max(v0, t[ie]))
            # three-shot: same experiment as twoshot, deploy optimum
            jd = deploy_best(model, [float(i0), float(i1)],
                             [v0, v1], n)
            scores["threeshot"].append(t[jd])
            # kg experiment: grid-search candidates
            best_kg, best_j = -np.inf, i1
            cand = range(0, n, max(1, n // 30))
            g_all = np.arange(n, dtype=float)
            for c in cand:
                if c == i0:
                    continue
                mu_c, var_c = posterior(model, np.array([float(i0)]),
                                        np.array([v0 - model["mean"]]),
                                        np.array([float(c)]))
                tot = 0.0
                for z, w in zip(zq, wq):
                    yv = mu_c[0] + np.sqrt(var_c[0] +
                                           model["s2_nug"]) * z
                    mu2, var2 = posterior(
                        model, np.array([float(i0), float(c)]),
                        np.array([v0 - model["mean"], yv]), g_all)
                    tot += w * np.max(np.exp(
                        mu2 + model["mean"]
                        + (var2 + model["s2_nug"]) / 2))
                if tot > best_kg:
                    best_kg, best_j = tot, c
            v1k = t[best_j]
            jd = deploy_best(model, [float(i0), float(best_j)],
                             [v0, v1k], n)
            scores["kg"].append(t[jd])
    print(f"held-out traces {len(test)}, episodes "
          f"{len(scores['incumbent'])}")
    # score on the objective the policies optimize: expected LINEAR
    # power, i.e. mean of exp(residual)
    base = np.mean(np.exp(scores["incumbent"]))
    for k in ("incumbent", "twoshot", "equispaced", "threeshot",
              "kg"):
        m = float(np.mean(np.exp(scores[k])))
        print(f"  {k:11s} mean linear payoff {m:7.3f}   "
          f"({(m / base - 1) * 100:+.1f}% vs incumbent)")

if __name__ == "__main__":
    traces = build_traces()
    print(f"traces: {len(traces)}")
    run_replay(traces)
