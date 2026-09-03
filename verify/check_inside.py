"""Check the Go Forth no-backtracking claim exactly.

Setup (paper, c=0): X is OU with kernel exp(-kappa|s-t|), unit
marginals. Observed X_0 = b and X_{t1} = d with lambda01 =
exp(-kappa t1). Final utility is E[exp(X_{t2})] = exp(mu + nu/2)
with (mu, nu) the conditional moments at the chosen t2.

Outside menu (Markov, anchored at the nearer observation y):
  mu = y * lam, nu = 1 - lam^2, lam in (0,1) free
  -> best log-utility from anchor y: zeta(y) = max_lam y*lam+(1-lam^2)/2
     = (y^2+1)/2 if 0<=y<=1, 1/2 if y<0 (lam->0), y if y>1.

Inside bridge point at correlations (lam2 to the 0 end, lam to the
t1 end), lam2*lam = lambda01:
  mu = (lam2(1-lam^2) b + lam(1-lam2^2) d) / (1-lambda01^2)
  nu = (1-lam2^2)(1-lam^2) / (1-lambda01^2)

Paper's p.22 chain asserts an outside point at rapidity
theta2+theta has the same mean and NO LESS variance, using
variance = sech(theta'). Truth: variance = sech^2(theta').
We test the consequence: is any inside point strictly better than
every outside choice? Exact Gaussian algebra + MC cross-check.
"""
import numpy as np

def zeta_log(y):
    if y < 0:
        return 0.5
    if y <= 1:
        return (y * y + 1) / 2
    return y

def bridge_moments(b, d, lam2, lam):
    lam01 = lam2 * lam
    den = 1 - lam01 ** 2
    mu = (lam2 * (1 - lam ** 2) * b + lam * (1 - lam2 ** 2) * d) / den
    nu = (1 - lam2 ** 2) * (1 - lam ** 2) / den
    return mu, nu

def best_inside_log(b, d, lam01, ngrid=2001):
    lam2s = np.linspace(np.sqrt(lam01) * 1e-6 + lam01, 1 - 1e-9, ngrid)
    lam2s = np.clip(lam2s, lam01 + 1e-9, 1 - 1e-9)
    best, arg = -np.inf, None
    for lam2 in lam2s:
        lam = lam01 / lam2
        if not (0 < lam < 1):
            continue
        mu, nu = bridge_moments(b, d, lam2, lam)
        u = mu + nu / 2
        if u > best:
            best, arg = u, (lam2, lam)
    return best, arg

def mc_check(b, d, lam01, lam2, lam, n=2_000_000, seed=0):
    """MC: sample X_mid | X_0=b, X_t1=d from exact conditional, and
    verify against a regression-free construction: simulate the
    trivariate OU Gaussian and condition by importance-free exact
    formula is circular; instead simulate the Markov chain forward
    exactly: X_mid | X_0=b ~ N(b*lam2, 1-lam2^2), then weight by the
    density of X_t1 = d | X_mid (Markov). Weighted moments must
    match the closed form."""
    rng = np.random.default_rng(seed)
    xm = b * lam2 + np.sqrt(1 - lam2 ** 2) * rng.standard_normal(n)
    w = np.exp(-0.5 * (d - lam * xm) ** 2 / (1 - lam ** 2))
    w /= w.sum()
    mu_mc = float(np.sum(w * xm))
    nu_mc = float(np.sum(w * xm ** 2) - mu_mc ** 2)
    eu_mc = float(np.sum(w * np.exp(xm)))
    return mu_mc, nu_mc, np.log(eu_mc)

if __name__ == "__main__":
    print("=== symmetric case d=b, t1 as the paper recommends "
          "(lambda01=b) ===")
    for b in (0.2, 0.3, 0.4, 0.45, 0.5, 0.7, 0.9):
        lam01 = b
        u_out = zeta_log(b)
        u_in, arg = best_inside_log(b, b, lam01)
        tag = "INSIDE WINS" if u_in > u_out + 1e-12 else "outside ok"
        print(f"b={b:.2f}: best inside {u_in:.5f}  best outside "
              f"{u_out:.5f}   {tag}")
    print()
    b = 0.5
    lam2 = lam = np.sqrt(0.5)     # middle of the bridge, lambda01=0.5
    mu, nu = bridge_moments(b, b, lam2, lam)
    mu_mc, nu_mc, logeu_mc = mc_check(b, b, 0.5, lam2, lam)
    print(f"middle bridge b=d=0.5, lam01=0.5: exact mu={mu:.4f} "
          f"nu={nu:.4f} logE[e^X]={mu+nu/2:.4f}")
    print(f"  MC (2m weighted): mu={mu_mc:.4f} nu={nu_mc:.4f} "
          f"logE[e^X]={logeu_mc:.4f}")
    print(f"  outside best (zeta): {zeta_log(b):.4f}")
    th = np.arctanh(lam2)
    print(f"  paper p.22 asserts outside var sech(2*theta2)="
          f"{1/np.cosh(2*th):.4f}; true outside var at matched mean "
          f"= sech^2 = {1/np.cosh(2*th)**2:.4f}; bridge var {nu:.4f}")
    print()
    print("=== asymmetric neighborhood: does inside still win for "
          "d near b? (b=0.5, lam01=0.5) ===")
    for d in (0.40, 0.45, 0.5, 0.55, 0.60, 0.70):
        u_out = max(zeta_log(b), zeta_log(d))
        u_in, _ = best_inside_log(b, d, 0.5)
        tag = "INSIDE WINS" if u_in > u_out + 1e-12 else "outside ok"
        print(f"d={d:.2f}: inside {u_in:.5f} outside {u_out:.5f}  {tag}")
