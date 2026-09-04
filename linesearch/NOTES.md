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

## exp2b: the full physics family (run 2026-09-03, run_family.py)
All 22 dynamics-simulating demos in example_applications, same
protocol (measure p, then the five-way head-to-head, budget 120).
Two axes now, not one:
- ROUGHNESS: grass mean rank 2.33/5 at p<1.1 vs 3.17 in the middle
  band. Every rank-1 rough demo is collision/agent chaos -- bowling
  p=0.29, boids_flocking p=0.19, plinko p=1.05, tennis_doubles
  p=0.90. But rough is NOT sufficient: free_kick (p=0.92) and
  tuned_mass_damper (p=1.06) are dead LAST -- both needle/resonance
  landscapes where value hides in a tiny region and golden's fixed
  full-segment probes are the right move; no placement theory helps
  when the signal is a spike. (trebuchet's slices came back constant,
  p=nan -- plateaus; golden wins it too.)
- DIMENSION, the unanticipated axis: mean rank 3.50 at d<=4 but
  2.25-2.50 at d>=5. wind_farm (d=16, p=1.61, SMOOTH slices) is a
  strong grass win -- 21-22/24 seeds vs golden2/brent -- and
  rocket_landing d=12 / satellite_phasing d=6 are near-wins
  (satellite 22/24 vs golden2 and random). In high d the per-line
  economy compounds: cheap lines buy direction coverage that
  expensive inner loops cannot afford.
So the sharpened claim: the grass inner loop wins when EITHER slices
are navigably rough (collision/agent chaos, p<~1.1 with spatial
structure, not needles) OR dimension is high enough that direction
count beats per-line precision. Classical inner loops keep low-d
smooth problems and all needle landscapes. Overall the rule is
rank 1 or 2 on 9 of 22 physical demos -- a real niche, plainly
bounded.

## exp2c/d/e: mechanism, the dimension law, and two new domains
(run 2026-09-04: run_ablations.py, run_dimsweep.py, run_nn_quant.py)

MECHANISM (ablations, all 22 demos). The engine is the per-line
economy plus the paper's Table-1 adaptive bracket, NOT the third-shot
endgame machinery:
- grass2 (two-shot only, 1 eval/line) ties or beats full grass3
  broadly, dramatically on rocket_landing (-75.9 vs -1.9) and
  cart_pole (-369 vs -214). This is Table 1's own "interior option
  is worth ~1%" resurfacing in the optimizer: the third shot's rival
  there is not nothing but a FRESH DIRECTION, and the fresh direction
  usually wins. The quartic/interior move is theory the outer loop
  cannot afford.
- Adaptivity is genuine: fixed-step es5 and localized golden2loc
  collapse on the rough family (plinko -1.25 / -0.4 vs grass -57),
  and frozen-kappa loses where scale matters (rocket +71 vs -1.9).
- Flee-to-segment-END has a cube-boundary bias (diagnosed on
  free_kick: 73/102 lines fled to an endpoint). Uniform-interior flee
  fixes darts_aim and satellite_phasing (best of family) and halves
  free_kick's gap, but needles still belong to golden2.
- wind_farm's high-d win survives every ablation; even es5 beats
  golden2 there. Short adaptive steps from a good anchor ARE the
  high-d mechanism.

DIMENSION LAW (classics at d=2..32, 24 seeds). Grass-vs-Brent seed
wins rise monotonically with d on all four objectives: rosenbrock
6/24 (d=2) -> 24/24 (d=32), griewank 6 -> 21, schwefel 6 -> 18,
rastrigin 4 -> 12; grass is rank 1 outright on rosenbrock and
griewank at d=8. The expensive inner loop fades as d grows; above
d~8 the real contest is between the two cheap-line methods, grass
and golden2.

NEW DOMAINS (Peter's suggestions). NN weight fitting
(teacher-student tanh MLP, d=33 and 73): grass beats golden6, Brent
and random decisively (16-23/24) but LOSES to golden2 (3-8/24) --
NN landscapes from random init reward occasional far jumps between
basins, golden2's specialty. Post-training quantization (per-channel
scales, 3-4 bit, d=17, measured slice p=1.21 -- inside the rough
band): golden2 wins again with random close behind; in-band
roughness is NOT sufficient when the good set is broad rather than
cascade-structured. Prompting / chain-of-thought optimization is the
natural few-expensive-evaluations regime for a 3-shot rule but needs
an LLM in the loop -- flagged as follow-up, not testable offline.

RECOMMENDED CONFIGURATION (grass2U: two-shot only + uniform-interior
flee, family rerun). The combination removes the rule's worst
failure mode while keeping its wins: free_kick -100.3 (grass3 was
-33, golden2 -105), rocket_landing -89.6 (grass3 -1.9), cart_pole
-350, with plinko/bowling/boids/tennis/wind_farm essentially
unchanged. Better median than grass3 on 12/22 demos and than golden2
on 10/22. This -- one model-placed probe per line, flee to a uniform
interior point, no third shot -- is the version to carry forward;
it is also the simplest.

STANDING RESULT. Across every experiment the quietly strongest
general baseline is golden2 -- two full-segment probes per line,
maximal direction economy with global reach and no model. The grass
rule's distinctive wins over it are the navigably-rough simulators
(bowling, plinko, boids, tennis) and structured high-d landscapes
(wind_farm, rosenbrock/griewank d~8-16); everywhere else the honest
recommendation is golden2, not Brent.
