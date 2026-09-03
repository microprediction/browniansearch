# Validation datasets for the One Last Trial case study

## UPDATE 2026-09-03 (Peter's parallel search): WiFi RSS shadowing
## displaces corn as the primary candidate
A WiFi RTT/RSS indoor-positioning dataset (Zenodo, CC BY 4.0 per the
report; DOI to be confirmed -- the closest record I located,
zenodo 17210359, has 4-AP RTT databases and does NOT match the
reported shape): 77,040 RSS measurements, 642 positions on a 92x15 m
floor, 13 access points, 120 repeats per position, ~50 contiguous
horizontal traces of 15+ locations. Peter's preliminary diagnostic
on detrended log mean power: skew 0.047, excess kurtosis -0.152,
pooled spatial correlation C(h) ~ 0.640 exp(-h/11.84) with R^2
0.990 -- expOU plus a nugget. TO REPRODUCE INDEPENDENTLY once the
DOI/file is in hand (house rule: rerun every number).

WHY THIS BEATS CORN: real measurements (not simulation), a natural
maximize-received-power deployment story (site survey: incumbent
measurement, one more survey point, commit a placement), AND a
35-year-old domain anchor -- log-power shadow fading with
EXPONENTIAL spatial correlation is the classical Gudmundson model
[U: read before citing], so the expOU premise is the standard model
of the field, not an assumption to defend.

Validation protocol (from the report): split by entire AP-corridor
traces, never random points; fit path loss, variance, correlation
length, nugget on training traces; treat the 120-sample mean power
as the dense latent payoff surface; replay the three-shot policy on
held-out traces snapping to the grid; compare terminal power vs
two-shot, no-interior, equispaced, and empirical knowledge-gradient
policies; report gains overall and conditional on the expOU
diagnostics passing. Secondary: Mostofi lab robotic RSS routes
(12,564 measurements at 2-5 cm spacing; academic-use restriction;
spatial averaging needed for fast fading).
(Agent reconnaissance 2026-09-03; 10 candidates checked for the
crux shape: many instances x dense grid on ONE controlled x.)

## Winner: Illinois APSIM corn nitrogen response
data.mendeley.com/datasets/xs5nbm4w55/1 (DOI 10.17632/xs5nbm4w55.1),
CC BY 4.0. 33 N rates, 0-320 kg/ha in 10 kg/ha steps -- a genuinely
dense 1-D grid -- over 4,270 fields x ~15 corn years (~60k+ curves,
~1.9M rows). Response: grain yield; PROFIT (yield value minus N
cost) is concave with a genuine interior optimum (the EONR), exactly
a deploy-worthy objective. Deterministic APSIM 7.10 simulation, so
the held-out 33-point curve is an unambiguous scoring target.
Protocol fit is exact: estimate the OU/GP covariance in N-rate from
OTHER fields, reveal the incumbent rate, place one trial, deploy,
score the profit gap against the field's own held-out curve.
THE CAVEAT TO DISCLOSE: simulated, not measured. Real-data analogues
(MRTN trials, cnrc.agron.iastate.edu; Ohio's 431 trials) have only
4-8 rates per site -- usable as a coarse companion check, not as the
dense scoring target.

## Runner-up: Tox21 15-point qHTS curves (via NTP ICE Curve Surfer,
ice.ntp.niehs.nih.gov, public domain; also EPA ToxCast invitrodb)
Real measurements, replicate noise quantified, tens of thousands of
concentration-response curves. Caveat: mostly monotone sigmoids, so
argmax is trivial -- the protocol survives only if deployment means
HITTING A TARGET EFFECT LEVEL (EC50/benchmark dose), a different but
legitimate objective.

## Secondary: LCBench + YAHPO (ML hyperparameter story)
35 tasks adequate for prior estimation, but dense 1-D slices come
from a SURROGATE, making ground truth a model. Honest only with that
stated.

## Rejected, with reasons worth remembering
Olympus (min dimension 3, no 1-D, 43 tasks thin); Summit/Baumgartner
(96 experiments); Perera Suzuki (categorical-dominated); Ahneman
Buchwald-Hartwig (all-categorical, fixed 60C); NIST AM Bench (real
1-D sweeps, ~handful of instances); Jominy (11-15 points x 126
steels but distance is a position, not a setting, and monotone); drc
teaching sets (too few). The eliminating pattern: chemistry HTE data
is few-instance multi-D sampled by optimizer trajectories, never
many-instance dense-1-D.
