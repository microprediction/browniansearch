# The humpday line-search angle (opened 2026-09-03)
Question (Peter): does the grass machinery help line search inside
derivative-free optimizers? A DFO line search IS terminal placement:
2-5 evaluations along a direction, then return a point. Classical
tools (golden section, Brent) assume smooth unimodal slices.

## exp1_slices: measured roughness of humpday objective slices
Variogram exponent p (E[(f(x+D)-f(x))^2] ~ D^p at small lags):
p=2 smooth (classical line search fine), p=1 OU (the paper's home).
- CLASSIC suite, direct random-line slices (d=3): p = 1.72-1.98.
  Smooth. No OU edge. (Peter predicted this and was right; so was
  his "horse will be smooth" -- measured 1.8-2.0.)
- MORTON-COMPOSED (space-filling-curve 1-D-ification, the original
  go_forth device): p tracks 2/d qualitatively -- d=2: 0.71-0.79
  (near OU), d=3: 0.23-0.60, d=4: 0.07-0.43 (sub-OU). Roughness is
  manufactured controllably; d=2 is the OU regime.
- PHYSICAL demos (example_applications, the JS-demo ports Peter
  pointed at): the spectrum. bowling p=0.29 (chain-reaction chaos,
  very rough), plinko_funnel p=1.34 (between OU and smooth),
  pool/trebuchet/mini_golf/curling p=1.91-1.99 (smooth ballistics).

## Where the OU line search lives, empirically
Bowling/plinko-class objectives (collision cascades) and
Morton-composed problems at low d. Smooth suites and smooth physics
are golden-section territory and should be said so plainly. Next:
(1) prior-art check on probabilistic line searches (Mahsereci-Hennig
JMLR 2017 is gradient-based/Wiener for SGD noise; ours would be
derivative-free, OU, closed-form terminal placement); (2) implement
the 3-evaluation grass rule as a line search; (3) benchmark inside
humpday on the rough family vs golden-section/Brent inner loops.

## exp2_bench: the head-to-head (run 2026-09-03)
All three "next" items done. (1) Prior art confirmed as characterized:
Mahsereci-Hennig (JMLR 18, 2017) is a GP line search for stochastic
GRADIENT descent -- integrated-Wiener model, gradient observations,
probabilistic Wolfe conditions, no closed-form placement; nothing
derivative-free/OU/terminal-placement-shaped found nearby. The niche
is open. (2) exp2_bench/ou3_linesearch.py implements the rule as an
inner line search: exact port of the paper's zeta / Table-1 rho*(b) /
stationarity quartic (verified to 0.0 against numerics2.py), with the
two oracle inputs estimated online -- standardization from running
mean/std, kappa by a chi^2_1-median-robust binned variogram fit.
Two adaptations were forced by practice and are documented in the
module: raw-pair storage (early pairs standardized against a
degenerate std poisoned the kappa fit, kappa -> 285, steps -> 0), and
plateau flight (on a flat region the collapsed sample std makes the
anchor look like b >> 1 and the rule near-stays forever; three barren
lines now break the tie toward the paper's own flee branch).

(3) Benchmark: one shared outer loop (iterated random-direction line
search, common start and direction stream per seed), budget 120
evals, inner loop the only difference. Medians over seeds:
- plinko_funnel (p=1.34, d=7): grass -56.4 BEATS golden2 -49.5,
  golden6 -47.9, random -46.9, Brent -28.3; 20-21/24 seed wins
  against every rival (binomial p ~ 1e-3). The headline.
- bowling (p=0.29, d=4): grass -104.5, best median of five, 6-8/12
  wins -- an edge, not significant alone at 12 seeds.
- pool/mini_golf/rosenbrock (smooth): Brent/golden6 win, as
  predicted and as should be said plainly; grass is close on pool,
  clearly behind on mini_golf and rosenbrock.
- Morton-composed d=2 (p~0.75): REFUTES the exp1 conjecture that
  this is grass's home. Random search wins outright and Brent (whose
  wide bracketing degenerates toward broad sampling) is second;
  grass only edges golden. Manufactured pure roughness has no
  navigable structure -- nothing for placement theory to exploit.

Verdict: the grass rule earns its keep in the middle band -- rough
but physically navigable landscapes (collision cascades), where its
1-2-eval lines let the outer loop see 3-5x more directions than
Brent's 8-10-eval lines, and its stay verdicts spend nothing. On
smooth slices classical inner loops win; on pure noise nothing beats
sampling. Roughness measured by p is necessary but not sufficient:
the edge needs p in roughly (0.3, 1.5) AND real spatial structure.
