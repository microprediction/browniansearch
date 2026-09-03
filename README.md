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

**When the Grass Really Is Greener: Three-Shot Search on an
Exponentiated Ornstein-Uhlenbeck Landscape** (Cotton) —
[papers/go_forth.pdf](papers/go_forth.pdf), source and numerics in
[papers/go_forth/](papers/go_forth/).

A searcher evaluates the landscape three times and is paid the value
at the final point. The two-shot policy is a closed-form three-phase
rule (flee / explore / stay). The three-shot question — go beyond the
bracket, or revisit its interior? — is settled by a rapidity
coordinate theta = tanh^-1(e^(-kappa dt)) under which bridge means
compose additively and bridge variances factor as
sech(theta2+theta)sech(theta2-theta): every interior point has the
same mean as the outside point at the composed rapidity and strictly
more variance, and the objective pays for variance. The bridge middle
beats every outside choice exactly when b^2(1+rho) - 4b sqrt(rho)
+ 2rho < 0 — stay between the anchors on good news; on bad news step
out past the better end, whichever end that is. The revisit
option is worth up to about one percent of expected value, and the
optimal bracket widens in anticipation of it.

Status: working paper. First version April 2022 (the original is
preserved in
[microprediction/home](https://github.com/microprediction/home/blob/main/workingpapers/go_forth.pdf),
first committed 2022-04-06); current version September 2026. Every
number is produced by `papers/go_forth/numerics.py` and independently
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
