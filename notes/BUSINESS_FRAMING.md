# One Last Trial: the business framing and the KG connection
(Peter's memo, 2026-09-03. Proposed application framing, not a
verified customer workflow.)

## The decision problem
"The last experiment before rollout": a manufacturer knows the
incumbent setting's performance, has time for ONE more pilot run,
then must deploy -- incumbent, tested alternative, or an untested
setting inside an approved operating range. That IS the three-shot
game: existing observation -> one experiment -> consequential
deployment (the final shot is the business decision, not a lab run).
The paper answers: where to put the last pilot knowing interpolation
follows; and afterward, interpolate / extrapolate / retain. KEY
QUALIFICATION: if deployment is restricted to individually tested
settings, the problem changes -- the target application must
genuinely allow interpolation within an approved range.

## The knowledge-gradient connection (add to the paper eventually)
With Q(D) = max_t E[e^{X_t} | D] the value of immediate deployment,
the value of testing s first is KG(s) = E_Y[Q(D + (s,Y))] - Q(D).
With one experiment remaining our optimal second location maximizes
exactly this: the three-shot game IS knowledge gradient with a
nonlinear (exponential) objective -- the generalized qKG that
BoTorch supports. Honest boundary: no new general experiment-
selection principle is claimed; the contribution is the unusually
explicit analysis (exact inner max via the quartic, exact phase
diagram) and possibly cheaper computation. Extension worth
benchmarking (deduction from Markov structure, not yet a result):
with many noiseless 1-D observations, a new interior experiment
changes only its containing interval -- everything else is a fixed
fallback -- so the bridge calculus gives inexpensive one-step
experiment scoring beyond the literal three-shot case.

## Audiences (plausible, not expressions of interest)
- Frazier / knowledge-gradient community: analytical benchmark for
  KG implementations and approximations (Frazier-Powell-Dayanik).
- Misener / BoFire industrial experimentation community (2025 paper;
  adoption reported at BASF, Evonik, Boehringer Ingelheim): the
  place to seek a real process dataset and a candid read on whether
  the decision setting occurs.

## The case study that would make it a business paper
ONE focused retrospective study, not speculative applications:
densely measured 1-D process-response curves from several production
jobs; prior estimated from OTHER jobs; reveal an incumbent result,
allow one experiment, score the DEPLOYED setting against held-out
measurements; compare vs incumbent reuse, engineering interpolation,
EI-based experimentation, correctly-specified KG. Score deployment
value after costs and quality penalties. Test observation noise,
finite operating limits, OU-misspecification. Do NOT promise the 1%
-- it measures one restriction under one model.

## Working title for the applied version
"One More Pivot" (Peter, 2026-09-03) -- strategy-audience framing,
subtitle to carry the placement question (e.g. "where to place a
final experiment, and when to settle between past successes").
Conditional on the pivot-count evidence verifying (agent out); if it
holds, the three-shot budget is the empirical regime, not a
tractability apology. "One Last Trial" remains the fallback if the
case study stays industrial/agronomic and the register clash with
pivot vocabulary matters. OU analysis as the exact benchmark, the
corn N-response dataset as the application.
