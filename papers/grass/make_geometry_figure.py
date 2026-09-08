"""Figure for the covariance-geometry section: the feasible terminal
correlation set C_rho in dimension >= 2, and the Euclidean triangle that
produces it. The paper's one-dimensional placements are exactly the
boundary of C_rho; the interior (the free candidate) is new above one
dimension.

Produces figures/geometry.pdf.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rho = 0.4

fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.4, 4.3))

# ---- Panel A: the Euclidean triangle (why the inequalities) ----
# two observations o1,o2 at distance -log rho; a terminal point t.
o1 = np.array([0.0, 0.0])
o2 = np.array([-np.log(rho), 0.0])
t = np.array([0.62 * (-np.log(rho)), 0.95])   # an interior candidate
for p, name, dx, dy in [(o1, "obs 1", -0.06, -0.16),
                        (o2, "obs 2", -0.02, -0.16),
                        (t, "terminal", 0.03, 0.06)]:
    axL.plot(*p, "o", color="tab:blue" if name != "terminal" else "tab:red", ms=7,
             zorder=3)
    axL.annotate(name, p, xytext=(p[0] + dx, p[1] + dy), fontsize=10)
for a, b, lab, mid in [(o1, o2, r"$-\log\rho$", 0.5),
                      (o1, t, r"$-\log x$", 0.5),
                      (o2, t, r"$-\log y$", 0.5)]:
    axL.plot([a[0], b[0]], [a[1], b[1]], "-", color="0.4", lw=1.2, zorder=2)
    m = a + mid * (b - a)
    axL.annotate(lab, m, fontsize=10, color="0.25",
                 ha="center", va="center",
                 bbox=dict(boxstyle="round,pad=0.1", fc="white", ec="none"))
axL.set_title("distances are triangle sides", fontsize=11)
axL.set_aspect("equal")
axL.axis("off")
axL.margins(0.2)

# ---- Panel B: the feasible correlation set C_rho ----
xs = np.linspace(1e-3, 1, 400)
# C_rho = { rho x <= y <= x/rho } and { x y <= rho }
# boundary vertices: origin, (rho,1) [=obs2], (1,rho) [=obs1]
# shade the region
X, Y = np.meshgrid(np.linspace(0, 1, 600), np.linspace(0, 1, 600))
feas = (X * Y <= rho) & (X >= rho * Y) & (Y >= rho * X)
axR.contourf(X, Y, feas.astype(float), levels=[0.5, 1.5],
             colors=["tab:blue"], alpha=0.14)

# boundary pieces: bracket arc (hyperbola) + two rays from the origin
arc = xs[(xs >= rho) & (xs <= 1)]
axR.plot(arc, rho / arc, color="tab:blue", lw=2.4,
         label=r"bracket $xy=\rho$")
axR.plot([0, rho], [0, 1], color="tab:green", lw=2.2,
         label=r"exterior rays $x=\rho y,\ y=\rho x$")
axR.plot([0, 1], [0, rho], color="tab:green", lw=2.2)

# key points (the one-dimensional placements sit on the boundary)
for p, name, dx, dy in [((1, rho), "obs 1", -0.20, 0.02),
                        ((rho, 1), "obs 2", 0.03, -0.02),
                        ((0, 0), "flee", 0.03, 0.02)]:
    axR.plot(*p, "o", color="tab:blue", ms=6, zorder=4)
    axR.annotate(name, p, xytext=(p[0] + dx, p[1] + dy), fontsize=9)
# the interior free candidate (b,d), genuinely inside C_rho
b, d = 0.50, 0.55
axR.plot(b, d, "s", color="tab:red", ms=8, zorder=5)
axR.annotate("free candidate\n" + r"$(x,y)=(b,d)$", (b, d),
             xytext=(b + 0.05, d + 0.05), fontsize=9, color="tab:red")

axR.set_xlim(0, 1.02)
axR.set_ylim(0, 1.02)
axR.set_xlabel(r"correlation $x$ to observation 1")
axR.set_ylabel(r"correlation $y$ to observation 2")
axR.set_title(r"feasible set $\mathcal{C}_\rho$ (dimension $\geq 2$, $\rho=0.4$)",
              fontsize=11)
axR.set_aspect("equal")
axR.legend(loc="lower right", fontsize=8, framealpha=0.9)
axR.annotate("interior:\nnew above 1-D", (0.34, 0.24), fontsize=8.5,
             color="0.35", ha="center")

fig.tight_layout()
fig.savefig("figures/geometry.pdf", bbox_inches="tight")
print("wrote figures/geometry.pdf")
