"""The commitment question: once inside a bracket, must you stay?

NO -- and the counterexample is provable, not just numerical. If the
revealed interior value v is at or below the process median (v <= 0)
while the outer anchors sit in [0,1], then EVERY point interior to
the two spoiled sub-brackets is weakly dominated by exiting to the
outside two-shot value zeta(b): for an interior point of the
sub-bracket (b, v, rho1) with correlations (lam2, lam) to the ends,

  mu  = A b + B v with A = lam2(1-lam^2)/(1-rho1^2) >= 0,
                       B = lam(1-lam2^2)/(1-rho1^2) >= 0,
  so mu <= lam2 b            (drop the nonpositive B v term; A <= lam2),
  nu  = (1-lam2^2)(1-lam^2)/(1-rho1^2) <= 1 - lam2^2,

  hence mu + nu/2 <= lam2 b + (1-lam2^2)/2 <= max_l [lb+(1-l^2)/2]
                  = zeta(b).

Strict when v < 0. So the naive commitment lemma is FALSE: a bad
draw sends the searcher back out.

What IS true (induction over the Bellman recursion, written up in
notes/COMMITMENT.md): the k-shot value function is nondecreasing in
every observed value, because all conditional means are nonnegative
combinations of observed values, all conditional variances are
value-free, and both effects push the same way. Exits are anchored
at OUTER values, so their worth does not depend on the interior
reveal v; stay-values increase in v; therefore the optimal stay/exit
decision is a THRESHOLD rule in v. This script measures the
threshold and spot-checks the monotonicity.
"""
import numpy as np

def zeta(y):
    if y < 0:
        return 0.5
    if y <= 1:
        return (y * y + 1) / 2
    return float(y)

def sup_interior(b, d, rho, ngrid=1200):
    lam2 = np.linspace(rho + 1e-9, 1 - 1e-9, ngrid)
    lam = rho / lam2
    den = 1 - rho ** 2
    mu = (lam2 * (1 - lam ** 2) * b + lam * (1 - lam2 ** 2) * d) / den
    nu = (1 - lam2 ** 2) * (1 - lam ** 2) / den
    return float(np.max(mu + nu / 2))

def stay_value(b, d, rho, v):
    """After revealing v at the middle of (b,d,rho): best interior
    placement in either sub-bracket (final shot)."""
    s = np.sqrt(rho)
    return max(sup_interior(b, v, s), sup_interior(v, d, s), v)

if __name__ == "__main__":
    b = d = 0.7
    rho = 0.5
    exit_val = max(zeta(b), zeta(d))
    print(f"bracket (b,d,rho)=({b},{d},{rho}); exit value "
          f"zeta = {exit_val:.4f}")
    print("revealed middle value v -> stay value (monotone?), "
          "decision:")
    prev = -np.inf
    for v in (-1.0, -0.5, -0.2, 0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.7,
              0.9):
        sv = stay_value(b, d, rho, v)
        mono = "ok" if sv >= prev - 1e-12 else "VIOLATION"
        prev = sv
        dec = "STAY" if sv > exit_val else "exit"
        print(f"  v={v:+.1f}: stay {sv:.4f}  [{dec}]  monotone {mono}")
    # threshold by bisection
    lo, hi = -1.0, 0.9
    for _ in range(60):
        mid = (lo + hi) / 2
        if stay_value(b, d, rho, mid) > exit_val:
            hi = mid
        else:
            lo = mid
    print(f"threshold: stay iff v > {hi:.4f}")
    # Proposition A margin: v <= 0 must always exit
    worst = max(stay_value(b, d, rho, v)
                for v in np.linspace(-3, 0, 61))
    print(f"Prop A check: sup over v<=0 of stay value {worst:.4f} "
          f"<= zeta(b) {exit_val:.4f}: {worst <= exit_val + 1e-9}")
