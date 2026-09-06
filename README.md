# browniansearch (view as [web page](https://browniansearch.microprediction.org))

*Few-shot search on Brownian-family paths.*

A searcher samples a rugged landscape — a path of a Brownian-family
process — a small number of times, and must decide where to sample
next. This repository is the home for that problem: optimal policies,
the distributional laws of path extremes that explain them, and code.

It is the search-side sibling of
[brownianbandit](https://github.com/microprediction/brownianbandit):
there a controller *prunes many* paths under budget; here a searcher
*samples one* path a few times. Both maximize an expected extreme.

## Founding paper

**When the Grass Is Greener: Three-Shot Search on an Exponentiated
Ornstein-Uhlenbeck Landscape** (Cotton) —
[papers/grass/grass.pdf](papers/grass/grass.pdf), source and numerics in
[papers/grass/](papers/grass/).

A searcher evaluates the landscape three times and is paid the value
at the final point -- terminal placement, not path-maximum
approximation. The two-shot policy is a closed-form three-phase rule
(flee / explore / stay). For a bracket of two equal observed values,
every interior point shares its conditional mean with an explicit
exterior point while carrying conditional variance larger by the
constant factor (1+rho)/(1-rho) = e^{2 Theta} -- matched-mean
dominance in the Gaussian convex order, for every convex payoff. The
symmetric interior problem is a constrained parabola bm + C(1-m^2)/2
whose clipped optimizer b/C yields the full phase diagram: the
interior beats every alternative exactly for b_-(rho) < b <
e^{2 Theta}; the optimal interior point is the middle only below
b = sinh(2 tau), beyond which mirror optima slide to the ends; and
above e^{2 Theta} the optimal final location is an OBSERVED one --
mean reversion caps every unvisited point's conditional mean, and
there the grass is provably not greener. The interior option is worth
about 1% of expected value at most (peak near b = 0.83), and most of
the three-shot bracket widening comes from the extra evaluation
itself.

Status: working paper. First version April 2022 (the original is
preserved in
[microprediction/home](https://github.com/microprediction/home/blob/main/workingpapers/go_forth.pdf),
first committed 2022-04-06); current version September 2026. Every
number is produced by `papers/grass/numerics2.py` and independently
checked by `verify/check_inside.py` (exact conditioning plus weighted
Monte Carlo).

## The static law behind the policy

The policy says go forth on bad news; the argmax law of the path
supplies the geometry: the maximum of a positively-correlated path
piles up at the boundary of any bracketed region, while the bridge
interior keeps the variance that an exponentiated objective pays
for. Exact finite-n laws of
the max, argmax, and first passage of Gauss-Markov paths — computed
by a transfer operator on a lattice, recovering Levy's arcsine law
in the random-walk limit — live in the
[winning](https://github.com/microprediction/winning) repository
(research/tridiagonal), and are the distributional complement of the
policy results here.

## Roadmap

- k-shot policies for k > 3, where closed forms die: value functions
  by dynamic programming on a lattice, using the rapidity coordinate
  as the natural discretization.
- Objectives beyond mean utility: P(beat the best seen), quantiles
  of the best-found, expected path maximum.
- The human-intuition survey, improved (a browser game).

## Related literature

Grill, Valko & Munos, *Optimistic optimization of a Brownian*
(NeurIPS 2018); Calvin, *Average performance of adaptive algorithms
for global optimization* (Ann. Appl. Prob. 1997); Callander,
*Searching for Good Policies* (APSR 2011); Baumann, Schmidt &
Stieglitz on rugged performance landscapes (J. Management 2019).
