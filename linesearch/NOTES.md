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
