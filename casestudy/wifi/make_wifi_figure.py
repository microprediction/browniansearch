"""Correlogram figure for the paper's empirical section: measured
pooled correlation of detrended log mean power along corridor
traces, with the fitted exponential."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# measured in diagnostic.py (this session's independent run)
lags = np.arange(1, 11)
corr = np.array([0.486, 0.437, 0.389, 0.359, 0.305, 0.288, 0.278,
                 0.234, 0.229, 0.222])
a0, L = 0.513, 11.03

fig, ax = plt.subplots(figsize=(4.6, 3.0))
ax.plot(lags * 0.6, corr, "ko", ms=5, label="measured (50 traces)")
hh = np.linspace(0.5, 10.5, 200)
ax.plot(hh * 0.6, a0 * np.exp(-hh / L), "tab:blue", lw=1.3,
        label=r"$0.51\,e^{-h/6.6\mathrm{m}}$  ($R^2=0.98$)")
ax.set_xlabel("separation (m)")
ax.set_ylabel("correlation of detrended log power")
ax.set_ylim(0, 0.55)
ax.legend(frameon=False, fontsize=8)
fig.tight_layout()
out = ("/Users/petercotton/github/browniansearch/papers/grass/"
       "figures/wifi_corr.pdf")
fig.savefig(out)
print("wrote", out)
