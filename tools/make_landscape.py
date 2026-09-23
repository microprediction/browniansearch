"""Landing picture: a mountain range drawn from exponentiated Ornstein-Uhlenbeck paths, with a few sampled points.

Writes docs/landscape.svg. Each ridge is exp(X) for a stationary OU path X; farther ridges are smoother, paler and
lower, the front ridge is the landscape a searcher samples, and the dots are its few evaluations.
"""
import numpy as np

W, H, N = 1200, 360, 900
rng = np.random.default_rng(11)


def ou(n, kappa, sigma, seed):
    r = np.random.default_rng(seed)
    dt = 1.0 / n
    a = np.exp(-kappa * dt)
    x = np.empty(n)
    x[0] = r.normal(0, sigma / np.sqrt(2 * kappa))
    s = sigma * np.sqrt((1 - a * a) / (2 * kappa))
    for i in range(1, n):
        x[i] = a * x[i - 1] + s * r.normal()
    return x


def ridge(seed, kappa, sd, base, height):
    x = ou(N, kappa, sd * np.sqrt(2 * kappa), seed)     # stationary standard deviation sd
    f = np.exp(x)
    return base - height * f / f.max()


layers = [  # (seed, kappa, stationary sd of the log, base, height, fill)
    (5, 2.5, 0.45, 215, 150, "#e7e5f5"),
    (8, 4.0, 0.50, 262, 175, "#cbc7eb"),
    (21, 7.0, 0.55, 310, 195, "#8f88cf"),
    (31, 10.0, 0.60, 360, 225, "#1f1d3d"),
]
xs = np.linspace(0, W, N)
parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
         f'aria-label="A rugged mountain range drawn from exponentiated Ornstein-Uhlenbeck paths, with a few sampled points">',
         '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#f7f6fd"/><stop offset="1" stop-color="#fafafa"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#sky)"/>']
front = None
for seed, k, s, base, h, fill in layers:
    y = ridge(seed, k, s, base, h)
    pts = " ".join(f"{a:.1f},{b:.1f}" for a, b in zip(xs, y))
    parts.append(f'<polygon points="0,{H} {pts} {W},{H}" fill="{fill}"/>')
    front = y
# a few-shot searcher: three evaluations on the front ridge
for frac in (0.30, 0.44, 0.37):
    i = int(frac * (N - 1))
    xx, yy = xs[i], front[i]
    parts.append(f'<line x1="{xx:.1f}" y1="{yy - 34:.1f}" x2="{xx:.1f}" y2="{yy - 7:.1f}" stroke="#4a3aff" '
                 f'stroke-width="2" stroke-dasharray="4 4"/>')
    parts.append(f'<circle cx="{xx:.1f}" cy="{yy:.1f}" r="6" fill="#4a3aff" stroke="#ffffff" stroke-width="2"/>')
parts.append('</svg>')
open('docs/landscape.svg', 'w').write("\n".join(parts))
print("wrote docs/landscape.svg")
