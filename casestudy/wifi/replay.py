"""The trace-split three-shot replay on the Feng WiFi floor.

Setup per held-out trace (a contiguous same-row run of 15+ grid
points for one AP): the detrended log-power residual r(s) is the
latent payoff surface, known densely from the 120-sample means. The
searcher sees the value at an incumbent grid point, places ONE more
measurement anywhere on the trace, then commits to a deployment
point on the trace; the score is exp of the true surface value at
the deployment.

Everything is fitted on training data only. Whole traces are split
first (seeded permutation, half each). The AP path-loss trend is
fitted on the location-AP observations outside the held-out traces
and frozen; held-out traces are detrended with the frozen fit. The
covariance model (residual variance s2, exponential correlation with
length L in grid units, nugget share) and the mean are fitted on the
training traces.

Policies compared (all see the same incumbent, same model). Only the
last is the three-shot rule; step_best is not the paper's two-shot
game, which pays the second point rather than the better of two:
  incumbent        deploy the incumbent point, no experiment
  step_best        experiment at correlation lam = clip(b, 0, 1)
                   from the incumbent (b = incumbent standardized by
                   the OU sd; the paper's two-shot step at s = 1),
                   deploy the better of the two observed points
  step_model       experiment as step_best, then deploy the model-
                   optimal point on the trace (see deploy_crit)
  far_best         experiment at the far end of the trace, deploy
                   the better observed point
  threeshot        the three-shot rule computed for the fitted trace
                   model: the trial maximizes the expected value of
                   the model-optimal deployment that follows it
                   (one-step lookahead over every grid point, Gauss-
                   Hermite over the trial's predictive value; finite
                   trace and nugget included), then deploy as
                   step_model
Deployment: an unobserved grid point j is worth
exp(mu_j + mean + (var_j + nugget)/2) under the model; an observed
point is worth exp of its known value. Deploy the argmax.
Scoring: exp of the true detrended surface value at the deployed
point, averaged over held-out traces and incumbent choices.

Data: Feng, Nguyen & Luo, Zenodo 11558192 (CC BY 4.0). Set
FENG_WIFI_DIR to the release's dataset/ directory, or unpack the
release zip into casestudy/wifi/data/.
"""
import json
import os
import numpy as np
import pandas as pd
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("FENG_WIFI_DIR", os.path.join(
    HERE, "data", "WiFi-RTT-RSS-dataset-main", "dataset"))


def build_obs():
    """Per location and AP: log of mean linear power over detected
    samples. The detection rule is fixed, not fitted."""
    df = pd.concat([pd.read_csv(os.path.join(BASE, f), sep="\t",
                                low_memory=False)
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
    return pd.DataFrame(recs, columns=["x", "y", "ap", "X"])


def find_traces(obs):
    """Contiguous same-row runs of 15+ grid points per AP, as arrays
    of obs row labels in x order. Uses geometry only."""
    traces = []
    for (ai, y), g in obs.groupby(["ap", "y"]):
        g = g.sort_values("x")
        xs = g["x"].values; ix = g.index.values
        run = [0]
        for i, st in enumerate(np.round(np.diff(xs)).astype(int)):
            if st == 1:
                run.append(i + 1)
            else:
                if len(run) >= 15:
                    traces.append(ix[run])
                run = [i + 1]
        if len(run) >= 15:
            traces.append(ix[run])
    return traces


def fit_trend(obs, fit_rows):
    """AP-wise log-distance path-loss trend with free AP position,
    fitted on fit_rows only; returns residuals for every row."""
    resid = pd.Series(np.nan, index=obs.index)
    for ai, g in obs.groupby("ap"):
        gf = g.loc[g.index.isin(fit_rows)]
        s = gf[["x", "y"]].values.astype(float)
        Xv = gf["X"].values
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
        sa = g[["x", "y"]].values.astype(float)
        dd = np.sqrt((sa[:, 0] - x0) ** 2 + (sa[:, 1] - y0) ** 2 + 0.25)
        resid.loc[g.index] = g["X"].values - (A - cc * np.log(dd))
    return resid


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

def deploy_crit(model, pts, vals, n):
    """Log expected payoff of deploying at each grid point: model
    value at unobserved points, the known value at observed ones."""
    grid = np.arange(n, dtype=float)
    mm = model["mean"]
    mu, var = posterior(model, np.asarray(pts, dtype=float),
                        np.asarray(vals) - mm, grid)
    crit = mu + mm + (var + model["s2_nug"]) / 2
    crit[np.asarray(pts, dtype=int)] = vals
    return crit


def deploy_best(model, pts, vals, n):
    return int(np.argmax(deploy_crit(model, pts, vals, n)))


def split_and_detrend(obs, traces, seed=0):
    rng = np.random.default_rng(seed)
    order = rng.permutation(len(traces))
    ntr = len(traces) // 2
    tr_idx, te_idx = order[:ntr], order[ntr:]
    held = np.concatenate([traces[i] for i in te_idx])
    fit_rows = obs.index.difference(held)
    resid = fit_trend(obs, fit_rows)
    train = [resid.loc[traces[i]].values for i in tr_idx]
    test = [resid.loc[traces[i]].values for i in te_idx]
    return rng, train, test


POLICIES = ("incumbent", "step_best", "step_model", "far_best",
            "threeshot")


def run_replay(obs, traces, seed=0, n_inc=5):
    rng, train, test = split_and_detrend(obs, traces, seed)
    model = fit_model(train)
    print(f"model: var {model['s2']:.3f}, L {model['L']:.2f}, "
          f"OU share {model['amp']:.2f}")
    scores = {k: [] for k in POLICIES}
    zq, wq = np.polynomial.hermite_e.hermegauss(15)
    wq = wq / wq.sum()
    mm, nug = model["mean"], model["s2_nug"]
    for t in test:
        n = len(t)
        for _ in range(n_inc):
            i0 = int(rng.integers(2, n - 2))
            v0 = t[i0]
            scores["incumbent"].append(v0)
            # step to correlation lam = clip(b, 0, 1) from the incumbent
            sdo = np.sqrt(model["s2_ou"])
            b = (v0 - mm) / sdo
            lam = min(max(b, 0.0), 1.0)
            step = max(1, int(round(-model["L"] * np.log(max(lam,
                       1e-6)))) if lam > 0 else n)
            i1 = i0 + step if i0 + step < n else max(0, i0 - step)
            i1 = int(np.clip(i1, 0, n - 1))
            v1 = t[i1]
            scores["step_best"].append(max(v0, v1))
            jd = deploy_best(model, [i0, i1], [v0, v1], n)
            scores["step_model"].append(t[jd])
            ie = n - 1 if i0 < n / 2 else 0
            scores["far_best"].append(max(v0, t[ie]))
            # three-shot trial: one-step lookahead over every grid point
            best_val, best_j = -np.inf, i1
            for c in range(n):
                if c == i0:
                    continue
                mu_c, var_c = posterior(model, np.array([float(i0)]),
                                        np.array([v0 - mm]),
                                        np.array([float(c)]))
                sd_c = np.sqrt(var_c[0] + nug)
                tot = 0.0
                for z, w in zip(zq, wq):
                    yv = mu_c[0] + mm + sd_c * z
                    crit = deploy_crit(model, [i0, c], [v0, yv], n)
                    tot += w * np.exp(crit.max())
                if tot > best_val:
                    best_val, best_j = tot, c
            jd = deploy_best(model, [i0, best_j], [v0, t[best_j]], n)
            scores["threeshot"].append(t[jd])
    print(f"held-out traces {len(test)}, episodes "
          f"{len(scores['incumbent'])}")
    # score on the objective the policies optimize: expected LINEAR
    # power, i.e. mean of exp(residual)
    pay = {k: np.exp(np.array(v)) for k, v in scores.items()}
    base = pay["incumbent"].mean()
    out = dict(model={k: float(v) for k, v in model.items()},
               n_train=len(train), n_test=len(test),
               episodes=len(scores["incumbent"]), policies={})
    for k in POLICIES:
        m = float(pay[k].mean())
        d = pay[k] - pay["incumbent"]
        se = float(d.std(ddof=1) / np.sqrt(len(d)))
        out["policies"][k] = dict(mean=m, gain=m / base - 1,
                                  se_vs_incumbent=se)
        print(f"  {k:11s} mean linear payoff {m:7.3f}   "
              f"({(m / base - 1) * 100:+.1f}% vs incumbent, "
              f"paired se {se:.3f})")
    d = pay["threeshot"] - pay["far_best"]
    out["threeshot_minus_far_best"] = dict(
        mean=float(d.mean()), se=float(d.std(ddof=1) / np.sqrt(len(d))))
    print(f"  threeshot - far_best {d.mean():+.3f} "
          f"(paired se {out['threeshot_minus_far_best']['se']:.3f})")
    return out


if __name__ == "__main__":
    obs = build_obs()
    traces = find_traces(obs)
    print(f"traces: {len(traces)}")
    out = run_replay(obs, traces)
    with open(os.path.join(HERE, "replay_results.json"), "w") as f:
        json.dump(out, f, indent=2)
