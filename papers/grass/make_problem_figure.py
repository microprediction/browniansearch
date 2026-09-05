"""Figure 1: the problem. A sampled exponentiated OU landscape with
two equal observed values, the posterior band, and the three
candidate final placements: stay at an anchor, settle between them,
or step out past an end."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(3)
kappa = 1.0
b = 0.7
t1 = -np.log(0.5) / kappa          # rho = 0.5
ts = np.linspace(-1.2, t1 + 1.6, 500)

# conditional mean and covariance of X given X(0)=X(t1)=b
obs_t = np.array([0.0, t1])
K = np.exp(-kappa * np.abs(ts[:, None] - obs_t[None, :]))
Koo = np.exp(-kappa * np.abs(obs_t[:, None] - obs_t[None, :]))
sol = np.linalg.solve(Koo, np.array([b, b]))
mu = K @ sol
Ktt = np.exp(-kappa * np.abs(ts[:, None] - ts[None, :]))
cov = Ktt - K @ np.linalg.solve(Koo, K.T)
sd = np.sqrt(np.clip(np.diag(cov), 0, None))

# one conditional sample path (the true landscape the searcher faces)
L = np.linalg.cholesky(cov + 1e-9 * np.eye(len(ts)))
path = mu + L @ rng.standard_normal(len(ts))

fig, ax = plt.subplots(figsize=(7.2, 3.2))
ax.fill_between(ts, np.exp(mu - sd), np.exp(mu + sd),
                color="tab:blue", alpha=0.15,
                label="posterior band for $f$")
ax.plot(ts, np.exp(mu), "tab:blue", lw=1.0, ls="--",
        label="posterior median $e^{\\mu}$")
ax.plot(ts, np.exp(mu + 0.5*np.diag(cov)), "tab:blue", lw=1.3,
        label="posterior mean $e^{\\mu+\\nu/2}$")
ax.plot(ts, np.exp(path), color="0.55", lw=0.8, alpha=0.9,
        label="one landscape consistent with the data")
ax.plot([0, t1], [np.exp(b)] * 2, "ko", ms=6, zorder=5)
ax.annotate("incumbent", (0, np.exp(b)), textcoords="offset points",
            xytext=(-10, 10), fontsize=9, ha="right")
ax.annotate("trial", (t1, np.exp(b)), textcoords="offset points",
            xytext=(8, 10), fontsize=9)
mid = t1 / 2
ax.axvline(mid, color="tab:green", lw=1.0, ls=":")
ax.annotate("between?", (mid, np.exp(mu[np.argmin(np.abs(ts - mid))]
                                     ) * 0.78),
            fontsize=9, color="tab:green", ha="center")
beyond = t1 + 0.55
ax.axvline(beyond, color="tab:red", lw=1.0, ls=":")
ax.annotate("beyond?", (beyond, 0.86), fontsize=9,
            color="tab:red", ha="center")
ax.annotate("stay?", (t1, np.exp(b)), textcoords="offset points",
            xytext=(8, -14), fontsize=9)
ax.set_xlabel(r"location $t$")
ax.set_ylabel(r"landscape $f(t)=e^{X_t}$")
ax.legend(frameon=False, fontsize=8, loc="upper left")
fig.tight_layout()
fig.savefig("figures/problem.pdf")
print("wrote figures/problem.pdf")
