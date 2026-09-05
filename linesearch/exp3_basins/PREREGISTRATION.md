# Pre-registration: budget-vs-basins hypothesis, faithful-port holdout
# WRITTEN BEFORE THE HOLDOUT SWEEP RESULTS EXIST (2026-09-04, before
# the humpday exp2k js_holdout emit). Every decision below is locked
# in advance; no choice may be revised after seeing the sweep.

## Hypothesis (Peter)
The rule wins when the evaluation budget is comparable to the number
of local minima the landscape presents. Few basins per line -> the
correlated bracket helps; many basins -> decorrelated spread wins.

## Primary test (locked)
Statistic: Spearman rank correlation between
  x = basins_per_line   (proxy below)
  y = grass2U benchmark rank   (tie-averaged, 1 = best)
over the HOLDOUT problems only.
Predicted sign: POSITIVE. Few basins -> low (good) rank; many basins
-> high (bad) rank; so more basins -> higher rank -> rho > 0.
Decision: hypothesis SUPPORTED if rho > 0 with p < 0.05 (one-sided,
direction predicted above); REFUTED if rho <= 0 or not significant.
Report rho, p, n, and the scatter regardless.

## Basin proxy (locked; identical to discovery exp3)
Per emitted 1-D slice of 257 points y[0..256]:
  g = diff(y); nsc = count of interior sign changes of g;
  basins = nsc/2 + 1.
basins_per_line = MEDIAN over the emitted slices per problem
(constant-slice / std < 1e-9 counts as basins = 1). Applied
identically to discovery and holdout. Sent to humpday for an
indicative column; this file's computation is the analysis of record.

## Rank definition (locked; identical to discovery)
Per problem, rank the six optimizers (grass2U, grassEI, golden2,
golden6, brent, random) by median-best value over seeds
(minimization), tie-averaged. grass2U's rank is y.

## Holdout membership (locked BEFORE seeing results)
Holdout = a JS demo page is INCLUDED iff its objective did NOT appear
in the 22-objective discovery set. EXCLUDED (seen in discovery,
contaminated): the five already-measured Matter demos -- pool,
curling, mini_golf, trebuchet, slingshot -- and any other JS page
whose objective is one of the discovery 22 (bowling, plinko_funnel,
boids_flocking, tennis_doubles, free_kick, goalkeeper_punt,
darts_aim, robot_arm, rocket_landing, satellite_phasing, wind_farm,
cart_pole_policy, walking_creature, brachistochrone, bridge_truss,
lennard_jones_cluster, tuned_mass_damper). The holdout is the
genuinely out-of-sample pages only.

## Prior (discovery) result, for the record
On the 22 contaminated ports: rho = -0.49, p = 0.02 (NEGATIVE,
against the hypothesis, but confounded by mislabeled-smooth ports).
On the exact exp(OU) control: consistent with POSITIVE (kappa up ->
grass rank up). The holdout adjudicates.

## What the paper does with each outcome (locked)
- Supported (rho>0, p<0.05): one sentence in the line-search
  discussion, budget-vs-basins as the operative axis, citing the
  holdout.
- Refuted or null: the hypothesis stays OUT of the paper; the
  existing economy/spread-vs-correlate wording stands unchanged.
No partial or reinterpreted outcome enters the paper.
