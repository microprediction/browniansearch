# WiFi case study: independent diagnostic reproduction (2026-09-03)
Dataset: Feng, Nguyen & Luo, "WiFi RTT RSS dataset for indoor
positioning", Zenodo 11558192, CC BY 4.0. Building floor: 92x15 m,
0.6 m grid (coordinates in grid units, X 0-125, Y 0-16), 642
reference points x 120 samples, 13 APs, 77,040 rows -- every number
matches the release README.

Reproduction (diagnostic.py) vs Peter's parallel run:
                        Peter          this session
  location-AP obs       4,387          4,235  (detection rule diff)
  traces >= 15          ~50            50
  residual skew         0.047          0.008
  excess kurtosis       -0.152         0.053
  C(h) fit              0.640 e^{-h/11.84}   0.513 e^{-h/11.03}
  R^2                   0.990          0.982

Two independent implementations (different detrending: this one fits
AP positions freely inside the path-loss model, since the release
does not tabulate them) agree: near-Gaussian residuals, exponential
spatial correlation with length ~11 grid units (~6.6-7.1 m), plus a
short-scale/nugget component of roughly half the variance. The expOU
premise holds on real radio measurements, consistent with the
classical Gudmundson shadowing model [U].

## Trace-split replay (replay.py, output in replay_results.json)
Protocol: split the 50 traces into 25 training and 25 held-out
traces first (seed 0). Fit the AP path-loss trend on the
location-AP observations outside the held-out traces and freeze it;
detrend the held-out traces with the frozen fit. Fit the covariance
model on the training traces: var 1.139, L = 9.43 grid units, OU
share 0.49. 125 episodes on the held-out traces, payoff exp of the
120-sample mean surface at the deployed point:

  trial              deployment        mean payoff   vs incumbent
  none               incumbent         2.899
  two-shot step      better observed   3.875         +33.7%
  two-shot step      model             4.235         +46.1%
  far end            better observed   4.300         +48.3%
  three-shot rule    model             4.380         +51.1%

threeshot - far_best: +0.079, paired se 0.260 (not distinguished).

The two-shot step is lam = clip(b, 0, 1) from the incumbent, b
standardized by the OU sd. With the better observed point paid it is
a heuristic, not the paper's two-shot game (which pays the second
point). The three-shot rule is the trial maximizing the expected
payoff of the model deployment that follows, computed on the finite
trace with the nugget by one-step lookahead over every grid point.
Model deployment values an observed point at its known value and an
unobserved one at exp(mu + (var + nugget)/2).

## Fast reversion
L ~ 9-11 against traces of 15-92: far probes are near-fresh draws.
Small-rho expansion of the exact formulas: revisit window
(b_-, e^{2 Theta}) -> (0.586 sqrt(rho), 1+2 rho) and the interior
premium U_off - zeta ~ rho (1 - b^2). The interior option's edge is
O(rho). That does not make measure-far-take-best optimal: the
exterior option keeps an O(1) value (zeta(y) > y for y < 1), and
the trial location still matters, even for the best of two
observed payoffs when the incumbent is positive. Adjacent points sit at rho = 0.91 (the slow
scale): one trace contains both scales.

## The multiscale program (Peter: PhD on fast mean-reverting OU;
## FPS-style singular perturbation)
epsilon = 1/(kappa T). Far probes become independent draws, but the
terminal point can still be stepped out from the best observation,
so the leading-order k-shot game is order statistics of independent
draws plus a two-shot exterior step from the best. Corrections:
bridge terms enter at O(epsilon) -- expand the exact three-shot
solution as the seed, then the k-shot value via the perturbation
machinery that closed forms cannot reach.

## Open items
1. Conditional cut: the phase diagram predicts where the three-shot
   rule beats far probing (high-b incumbents, near brackets); report
   gains conditional on the incumbent's standardized b and position.
2. Trace-level mean effects: detected traces have elevated mean; a
   per-trace random intercept (AP-corridor effect) is not in the
   model and may misallocate variance between mean and OU.
3. More episodes or several splits, to separate the leading
   policies.
