"""The sigma-parabola reduction and the full algebraic proof, checked.

  1. f depends on x only through sigma = x + rho/x:
     f = b sigma/(1+rho) + ((1+rho)^2 - sigma^2)/(2(1-rho^2)),
     peak at sigma* = b(1-rho); range sigma in [2 sqrt(rho), 1+rho).
  2. Off-middle optimum U_off = (b^2 e^{-2T} + e^{2T})/2, T=artanh(rho):
     - U_off - b = e^{-2T}(b - e^{2T})^2 / 2  (AM-GM tangency)
     - U_off - (b^2+1)/2 = (e^{2T}-1)(1 - b^2 e^{-2T})/2 > 0 for b<=1.
  3. No-gap inequalities closing the middle regime:
     (a) rho <= 3-2sqrt2:  b_+ >= sinh 2tau  <=>  (1-rho)^3 >= 8 rho^2
     (b) rho >= 3-2sqrt2:  b_+ >= 1  <=>  2u^2(1+u) >= (1-u)^3, u=sqrt(rho)
     (c) b>1 middle regime: U_mid >= b up to (1+u)/(2(1-u)) >= sinh 2tau.
"""
import numpy as np

rng = np.random.default_rng(0)
ok = True
for _ in range(200000):
    rho = rng.uniform(0.001, 0.999)
    x = rng.uniform(rho + 1e-6, 1 - 1e-6)
    b = rng.uniform(0, 3)
    lam = rho / x
    mu = b * (x + lam) / (1 + rho)
    nu = (1 - x * x) * (1 - lam * lam) / (1 - rho * rho)
    f_direct = mu + nu / 2
    sig = x + lam
    f_sigma = b * sig / (1 + rho) + ((1 + rho) ** 2 - sig ** 2) / (
        2 * (1 - rho ** 2))
    if abs(f_direct - f_sigma) > 1e-10:
        ok = False
        break
print("1. sigma reduction identity over 200k random draws:", ok)

e2t = lambda rho: (1 + rho) / (1 - rho)
bad = 0
for _ in range(100000):
    rho = rng.uniform(0.001, 0.999)
    st = 2 * np.sqrt(rho) / (1 - rho)
    b = rng.uniform(st, e2t(rho))          # off-middle regime
    uoff = 0.5 * (b * b / e2t(rho) + e2t(rho))
    lhs1 = uoff - b
    rhs1 = (b - e2t(rho)) ** 2 / (2 * e2t(rho))
    if abs(lhs1 - rhs1) > 1e-9:
        bad += 1
    if b <= 1:
        lhs2 = uoff - (b * b + 1) / 2
        rhs2 = (e2t(rho) - 1) * (1 - b * b / e2t(rho)) / 2
        if abs(lhs2 - rhs2) > 1e-9 or lhs2 <= 0:
            bad += 1
print("2. U_off identities (AM-GM square + b<=1 positivity):",
      "ok" if bad == 0 else f"{bad} FAILURES")

r0 = 3 - 2 * np.sqrt(2)
rr = np.linspace(1e-4, r0, 5000)
a_ok = np.all((1 - rr) ** 3 >= 8 * rr ** 2 - 1e-12)
uu = np.sqrt(np.linspace(r0, 1 - 1e-4, 5000))
b_ok = np.all(2 * uu ** 2 * (1 + uu) >= (1 - uu) ** 3 - 1e-12)
uu2 = np.sqrt(np.linspace(1e-4, 1 - 1e-4, 5000))
c_ok = np.all((1 + uu2) / (2 * (1 - uu2))
              >= 2 * uu2 ** 2 / (1 - uu2 ** 2) - 1e-12)
print(f"3. no-gap inequalities: (a) {a_ok} (b) {b_ok} (c) {c_ok}")
