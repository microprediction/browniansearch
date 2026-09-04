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

Next: the trace-split three-shot replay per the recorded protocol
(prior fit on training traces only; 120-sample mean power as the
latent payoff surface; policies compared: three-shot exact,
two-shot, interior-excluded, equispaced, empirical KG).

## Replay round one (2026-09-03, scoring corrected to the
## exponential payoff the policies optimize)
Model fit on 25 training traces: var 1.165, L = 10.77 grid units,
OU share 0.50. 125 episodes on 25 held-out traces:
  incumbent    2.596 linear payoff   (baseline)
  twoshot      3.184  (+22.6%)
  threeshot    3.442  (+32.5%)
  kg           4.224  (+62.7%)
  equispaced   4.409  (+69.8%)
(A first run scored mean LOG power -- the wrong exam for policies
optimizing E[e^X]; corrected before reading anything into it.)

## The standings are the theory's own fast-reversion prediction
L ~ 11 against traces of 15-92: far probes are near-fresh draws.
Small-rho expansion of the exact formulas: revisit window
(b_-, e^{2 Theta}) -> (0.586 sqrt(rho), 1+2 rho) and the interior
premium U_off - zeta ~ rho (1 - b^2): the interior option's edge is
O(rho) while the fresh-draw variance bonus is O(1). Fast mean
reversion demotes revisiting to a second-order refinement, so
measure-far-take-best is leading-order optimal -- equispaced and KG
lead because the regime says they should. Adjacent points sit at
rho = 0.91 (the slow scale): one trace contains both scales.

## The multiscale program (Peter: PhD on fast mean-reverting OU;
## FPS-style singular perturbation)
epsilon = 1/(kappa T). Leading order: the k-shot game degenerates to
order statistics of independent draws plus the incumbent (a winning-
engine object). Corrections: bridge terms enter at O(epsilon) --
expand the exact three-shot solution as the seed, then the k-shot
value via the perturbation machinery that closed forms cannot reach.
This would give the paper an asymptotic k-shot section grounded in
exactly the regime the real data occupies.

## Honest gaps in round one, to fix in round two
1. Conditional cut missing: the phase diagram predicts WHERE
   threeshot beats far-probing (high-b incumbents, near brackets);
   report gains conditional on the incumbent's standardized b and
   the region, not just pooled.
2. Trace-level mean effects: detected traces have elevated mean
   (+0.39); a per-trace random intercept (AP-corridor effect) is not
   in the model and may misallocate variance between mean and OU.
3. Finite-trace flee: the theory's "flee to infinity" maps to the
   far end of a short trace; twoshot/threeshot implementations
   truncate the step rather than model the boundary.
