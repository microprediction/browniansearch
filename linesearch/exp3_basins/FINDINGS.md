# Budget-vs-basins hypothesis: confounded on the ports, clean on OU
(Peter's hypothesis: the rule works when trials are not much more
than the number of local minima. Tested 2026-09-04.)

## Two datasets disagree on the sign
- exp(OU) exact control (kappa = basin count per line, clean):
  MORE basins -> grass WORSE (d=16: kappa 3 rank 2.0, kappa 10/30
  rank 5.0). SUPPORTS the hypothesis.
- physics ports (count_basins.py, basins = gradient sign-changes on
  1-D slices): Spearman(basins, grass_rank) = -0.49, p=0.02 -- MORE
  basins -> grass BETTER. OPPOSITE sign.

## Why: the physics-port test is contaminated
The low-basin physics cases are exactly the reduced-order ports we
already found mislabeled-smooth: pool 1.5, curling 1.0, mini_golf
1.5, trebuchet 1.5, goalkeeper 1.5 -- all with BAD grass ranks
(9,9,10,8,7). On the TRUE JS physics these are collision-rough
(pool p=0.15, curling p=0.07), i.e. MANY basins, and grass still
loses there (broad probes win). So the true points would flip from
(few basins, grass loses) to (many basins, grass loses), collapsing
the port correlation and plausibly reconciling toward the OU sign.
The port basin counts are unreliable precisely where the hypothesis
is decided.

## Conclusion
The hypothesis is NOT settled. The clean control supports it; the
physics test is confounded by the reduced-order ports and cannot be
trusted at its measured sign. Resolving it needs basin counts and
win/loss on FAITHFUL physics -- the holdout Peter proposed. The
humpday session is porting the true JS demos headless; the holdout
should be built there, not by duplicating 79 ports here. Do NOT put
the basin hypothesis in the paper until the faithful-port holdout
decides it; the paper's current regime wording (economy + spread-vs-
correlate) stands and does not depend on it.

## HOLDOUT VERDICT (2026-09-05): SUPPORTED, pre-registered
Locked test on the js_holdout sweep (run_holdout_test.py): 34 out-of-
sample pages after the pre-registered exclusions (16 discovery-
overlapping/seen demos dropped). Spearman(basins, grass2U_rank) =
+0.452, one-sided p=0.0036 -- predicted sign, past the pre-registered
p<0.05 threshold. Robustness: the highest-basin page (chess, 48.8
basins, rank 2.0) runs AGAINST the hypothesis, so dropping it
strengthens to +0.506 (p=0.0026); the result is not propped up by an
outlier. Caveat retained: 16/34 pages are smooth (basins=1.0 tied),
so the signal is carried by the rougher tail; this is one pre-
registered holdout correlation, stated as such in the paper, not a
law. Per the pre-registration, one sentence added to the line-search
discussion; the economy/spread-vs-correlate wording is unchanged.

## Correction (2026-09-05): punt_the_wire excluded, n=33 of record
The humpday session flagged punt-the-wire.html as goalkeeper_punt's
JS original (lock-step parity, same objective/constants -- a standing
demo-pair rule, not a name inference), so the locked exclusion "any
JS page whose objective is one of the discovery 22" applies. Rerun on
33: Spearman(basins, grass_rank) = +0.455, one-sided p=0.0039 --
verdict unchanged, SUPPORTED. Paper carries the n=33 figures.
