# How far the three-shot result generalizes
(Assessment 2026-09-03, on Peter's question. Ranked by how much
structure survives; the first two are theorems, the rest are
programs.)

## 1. Every convex payoff at once (theorem, free)
The dominance theorem is secretly a convex-order statement. Two
Gaussians with the same mean and ordered variances are ordered in the
convex order (N(mu,v1) = N(mu,v2) + independent noise, v1>v2), so the
interior bridge point -- same mean as its mean-matched outside rival,
strictly more variance -- dominates it for EVERY convex payoff
simultaneously, not just exp. The exp case merely makes the boundary
quadratic closed-form. Dual, equally clean: for CONCAVE payoffs the
ordering flips -- a risk-averse searcher (concave utility of height)
should never prefer the uncertain patch at equal expected height; the
grass is provably browner. One family of results parametrized by the
searcher's risk attitude, with the lognormal sitting at the exactly-
solvable point.

## 2. Every Gauss-Markov process (theorem, nearly free)
Rapidity additivity is just multiplicativity of correlation over
disjoint intervals, which holds for ANY Gauss-Markov process (time-
varying kappa, non-stationary variance) after the deterministic time
change theta(t). The whole analysis -- bridge mean composition,
variance product, dominance, boundary -- carries with theta the
natural clock. The Brownian limit (kappa -> 0) is degenerate and
explains why OU is the right home: BM is a martingale, so every
outside point keeps its anchor's mean while variance grows linearly;
going forth is free variance at constant mean and the searcher walks
to the horizon. Mean reversion is what makes the trade a trade.

## 3. k shots (program: segment-splitting DP)
By the Markov property the posterior after any sample set factorizes
into independent bridges between neighbors plus two outer rays, so
the k-shot state is the sorted frontier of (location, value) pairs
and each new sample splits one segment. Value iteration on a lattice
(rapidity-spaced) is cheap per step with the closed bridge moments.
Conjecture from the three-shot endgame: two phases -- step out past
the running best while values climb, refine between the two best once
a good region is bracketed. Genuine exploration (information for
later shots) enters here and nowhere in the three-shot game.

## 4. Trees, bands, noise (programs, harder)
- TREES: exponential-kernel processes on a metric tree keep the
  Markov/bridge structure (samples split subtrees); the winning tree
  cavity is the pricing engine. Search on R^d does not reduce except
  through space-filling curves at the cost of Hoelder roughness.
- BAND-DIAGONAL (AR(p)): bridges see p neighbors; closed forms die,
  the lifted-state lattice from winning/research/tridiagonal prices
  it numerically.
- NOISY OBSERVATIONS: bridges become GP/Kalman posteriors; rapidity
  survives in state-space form. The three-shot game is then the
  exactly-solvable toy of Bayesian optimization -- worth framing as
  such.

## 5. Threshold objectives = correlated pass@k (the bridge outward)
Change the payoff to P(find f > y in k samples) and browniansearch
becomes the STRUCTURED CORRELATED-ATTEMPTS model that the pass@k
literature lacks (winning/research/evalstats: everyone assumes
exchangeable attempts; the closest work has only mixture-induced
correlation). Attempts = locations on a correlated landscape;
attempt correlation = e^(-kappa dt), dialed by proximity; coverage
curves, optimal spacing of attempts, and the diversity-vs-fidelity
trade all become computable with the max/argmax/first-passage laws
(winning/research/tridiagonal exp1-3). The searcher's question "how
far apart should my k attempts be" is exactly the redundancy question
eval people wave at. This is the generalization with an external
audience.
