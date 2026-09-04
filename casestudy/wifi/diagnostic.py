"""Independent reproduction of the expOU diagnostic on the Feng
WiFi RTT/RSS building-floor dataset (Zenodo 11558192, CC BY 4.0).

Per location s and AP a: mean linear power over the ~120 repeats,
Pbar = mean(10^(RSS/10)) over detected samples (RSS > -200), and
X = log Pbar. Remove an AP-specific log-distance path-loss trend
with the AP position fitted (positions are not tabulated in the
release): X ~ A - c * log ||s - s0||, free (A, c, s0). Report
moments of the residual and the pooled spatial correlation over
lags 1-10 along contiguous same-row traces.

Target (Peter's parallel run): 4,387 location-AP observations,
~50 traces of 15+, skew 0.047, excess kurtosis -0.152,
C(h) ~ 0.640 exp(-h/11.84), R^2 0.990.
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import skew, kurtosis

BASE = ("/private/tmp/claude-501/-Users-petercotton-github-winning/"
        "4cfe1164-1ade-46c7-a29a-33bedf35fe90/scratchpad/wifi_feng/"
        "WiFi-RTT-RSS-dataset-main/dataset/")

def load():
    fr = pd.read_csv(BASE + "dataset_building_floor_train.csv",
                     sep="\t")
    te = pd.read_csv(BASE + "dataset_building_floor_test.csv",
                     sep="\t")
    df = pd.concat([fr, te], ignore_index=True)
    return df

if __name__ == "__main__":
    df = load()
    rss_cols = [c for c in df.columns if "RSS" in c]
    print(f"rows {len(df)}, APs {len(rss_cols)}, "
          f"positions {df.groupby(['X','Y']).ngroups}")
    # per-location mean linear power per AP
    recs = []
    for (x, y), g in df.groupby(["X", "Y"]):
        for ai, c in enumerate(rss_cols):
            r = g[c].values.astype(float)
            det = r > -150
            if det.sum() >= 30:            # detected most of the time
                pbar = np.mean(10 ** (r[det] / 10))
                recs.append((x, y, ai, np.log(pbar)))
    obs = pd.DataFrame(recs, columns=["x", "y", "ap", "X"])
    print(f"location-AP observations: {len(obs)}")

    # AP-wise path-loss detrend with fitted AP position
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
            r = minimize(nll, init, method="Nelder-Mead",
                         options=dict(maxiter=4000, xatol=1e-4))
            if best is None or r.fun < best.fun:
                best = r
        x0, y0, A, cc = best.x
        dd = np.sqrt((s[:, 0] - x0) ** 2 + (s[:, 1] - y0) ** 2 + 0.25)
        obs.loc[g.index, "resid"] = Xv - (A - cc * np.log(dd))
    r = obs["resid"].values
    print(f"residual moments: skew {skew(r):.3f}, "
          f"excess kurtosis {kurtosis(r):.3f}, sd {np.std(r):.3f}")

    # contiguous same-row traces per AP (grid step 0.6m in x)
    traces = []
    for (ai, y), g in obs.groupby(["ap", "y"]):
        g = g.sort_values("x")
        xs = g["x"].values; rs = g["resid"].values
        step = np.round(np.diff(xs)).astype(int)
        run = [0]
        for i, st in enumerate(step):
            if st == 1:
                run.append(i + 1)
            else:
                if len(run) >= 15:
                    traces.append(rs[run])
                run = [i + 1]
        if len(run) >= 15:
            traces.append(rs[run])
    print(f"contiguous traces of 15+: {len(traces)}")

    # pooled correlation over lags 1..10 (grid units)
    lags = np.arange(1, 11)
    corr = []
    for h in lags:
        a, b = [], []
        for t in traces:
            if len(t) > h:
                a.append(t[:-h]); b.append(t[h:])
        a = np.concatenate(a); b = np.concatenate(b)
        corr.append(np.corrcoef(a, b)[0, 1])
    corr = np.array(corr)
    # fit a * exp(-h/L)
    good = corr > 0
    coef = np.polyfit(lags[good], np.log(corr[good]), 1)
    L = -1 / coef[0]; a0 = np.exp(coef[1])
    pred = a0 * np.exp(-lags / L)
    ss = 1 - np.sum((corr - pred) ** 2) / np.sum(
        (corr - corr.mean()) ** 2)
    print(f"pooled correlation fit: C(h) = {a0:.3f} exp(-h/{L:.2f}),"
          f" R^2 = {ss:.3f}")
    print("lags:", " ".join(f"{c:.3f}" for c in corr))
