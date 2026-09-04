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
