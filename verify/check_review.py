"""Verify every claim in the September review before editing.

 1. Variance ratio nu_in/nu_out at matched mean is CONSTANT
    (1+rho)/(1-rho) across the bracket (not endpoint-degenerate).
 2. b=d=4, rho=0.5: staying at an anchor beats every unobserved
    location (e^{2Theta}=3 < 4).
 3. Asymmetric counterexample: b=0.5, rho=0.5, d=1:
    L(x)-1 = -(2x-1)^2 (x^2+x+1) / (6 x^2) < 0 on (1/2, 1).
 4. General stationarity quartic:
    x^4 - (b - rho d) x^3 + rho (d - rho b) x - rho^2 = 0.
 5. Exact flee limit at b<0: 1/2 + log(1 + 1/sqrt(2 pi)).
"""
import numpy as np

def bridge(b, d, rho, x):
    lam = rho / x
    den = 1 - rho * rho
    mu = (x * (1 - lam ** 2) * b + lam * (1 - x ** 2) * d) / den
    nu = (1 - x ** 2) * (1 - lam ** 2) / den
    return mu, nu

# 1. constant variance ratio
rng = np.random.default_rng(1)
worst = 0.0
for _ in range(100000):
    rho = rng.uniform(0.01, 0.99)
    x = rng.uniform(rho + 1e-6, 1 - 1e-6)
    th2, th = np.arctanh(x), np.arctanh(rho / x)
    nu_in = 1 / (np.cosh(th2 + th) * np.cosh(th2 - th))
    nu_out = 1 / np.cosh(th2 + th) ** 2
    ratio = nu_in / nu_out
    worst = max(worst, abs(ratio - (1 + rho) / (1 - rho)))
print(f"1. ratio == (1+rho)/(1-rho): max deviation {worst:.2e}")

# 2. stay wins at b=d=4, rho=0.5
b = d = 4.0; rho = 0.5
xs = np.linspace(rho + 1e-6, 1 - 1e-6, 200001)
mu, nu = bridge(b, d, rho, xs)
sup_in = np.max(mu + nu / 2)
# best unobserved outside: anchor 4, log-value max_l 4l+(1-l^2)/2 = 4 at l=1 (revisit) else <4
out_l = np.linspace(1e-6, 1 - 1e-6, 200001)
sup_out = np.max(4 * out_l + (1 - out_l ** 2) / 2)
print(f"2. b=d=4,rho=0.5: sup interior {sup_in:.4f}, sup unvisited "
      f"outside {sup_out:.4f}, stay pays {4.0:.4f} -> stay wins: "
      f"{4.0 > max(sup_in, sup_out)}")

# 3. d=1 factorization
b, rho, d = 0.5, 0.5, 1.0
xs = np.linspace(0.5 + 1e-9, 1 - 1e-9, 30001)
mu, nu = bridge(b, d, rho, xs)
L = mu + nu / 2
rhs = -((2 * xs - 1) ** 2) * (xs ** 2 + xs + 1) / (6 * xs ** 2)
ok_id = np.max(np.abs(L - 1 - rhs)) < 1e-12
ok_sign = np.all(rhs < 0)          # the factored form is negative on
                                   # the strict interior; testing L<1
                                   # directly hits fp cancellation at
                                   # the endpoint
assert ok_id and ok_sign
print(f"3. d=1 identity max|L-1-rhs| = {np.max(np.abs(L - 1 - rhs)):.2e}"
      f"; factored expression negative on strict interior: {ok_sign}")

# 4. quartic stationarity
bad = 0
for _ in range(20000):
    rho = rng.uniform(0.02, 0.95)
    b, d = rng.uniform(-1, 2, 2)
    x = rng.uniform(rho + 0.01, 0.99)
    eps = 1e-6
    mu1, nu1 = bridge(b, d, rho, x + eps)
    mu0, nu0 = bridge(b, d, rho, x - eps)
    fp = ((mu1 + nu1 / 2) - (mu0 + nu0 / 2)) / (2 * eps)
    quart = (x ** 4 - (b - rho * d) * x ** 3 + rho * (d - rho * b) * x
             - rho ** 2)
    # f' and quartic should vanish together: compare f' with
    # -quart/(x^3 (1-rho^2)) (sign/normalization from derivation)
    pred = -quart / (x ** 3 * (1 - rho ** 2))
    if abs(fp - pred) > 1e-4 * max(1, abs(fp)):
        bad += 1
print(f"4. quartic matches f' analytically: {bad} failures / 20000")

# 5. exact flee limit
from scipy.stats import norm
from scipy.integrate import quad
def zeta(y):
    return 0.5 if y < 0 else ((y * y + 1) / 2 if y <= 1 else y)
val, _ = quad(lambda z: norm.pdf(z) * np.exp(zeta(z)), -12, 12,
              limit=200)
exact = 0.5 + np.log(1 + 1 / np.sqrt(2 * np.pi))
print(f"5. flee limit: quadrature {np.log(val):.9f} vs closed form "
      f"{exact:.9f}")
