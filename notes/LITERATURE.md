# Reading notes: the Callander Brownian-landscape search tradition
(Assembled 2026-09-03 from four reading agents, each instructed to
read introductions, models, and main results at source, with access
labeled. Purpose: couch the grass paper properly -- one strand per
paragraph, engaging specific papers. Format per paper: CITE, MODEL,
MAIN RESULTS, METHOD, SHOTS, RELATION, QUOTE.)

## KEY COUCHING FACTS SURFACED BY THE READS
1. Bardhi (Econometrica 2024) Theorem: within powered-exponential
   covariances, ONLY p=1 -- the OU kernel -- satisfies the
   nearest-attribute (Markov) property. The literature's own license
   for the (exponentiated) OU landscape as the natural non-Brownian
   primitive. Quote: "the only covariance that satisfies NAP within
   this class is that corresponding to p = 1. This is the covariance
   of the well-known Ornstein-Uhlenbeck (OU) process." (S2.3 p10.)
2. Urgun-Yariv (JPE 2025) name OU terrains only as a possible
   extension (their fn. 6).
3. Strand-C synthesis: the tradition bifurcates into (a) continuous-
   trajectory search on driftless Brownian terrain with drawdown
   stopping and flow/running-max payoffs, and (b) finite point-
   evaluation designs where samples are an infinite per-period
   sequence or a single simultaneous estimation batch. No paper
   solves a fixed small budget of sequential point evaluations with
   terminal-placement payoff and exact closed-form phase boundaries.

============================================================
## STRAND C: INDEPENDENT ECONOMICS ADOPTERS (complete, read at
## source; local PDFs cached in the session scratchpad)

[Strand C notes: seven papers -- Garfagnini & Strulovici ReStud 2016;
Bardhi Econometrica 2024; Bardhi & Bobkova JPE 2023; Urgun & Yariv
JPE 2025; Cetemen, Urgun & Yariv JPE 2023; Wong TE 2025; Carnehl &
Schneider Econometrica 2025 -- full structured notes delivered by the
reading agent and stored verbatim in
casestudy/../notes/strand_c.md alongside; key facts hoisted above.]

============================================================
## STRAND D: REMAINING ADOPTERS AND THE CS LINE (complete)

KEY FACTS:
- AYBAS & CALLANDER (WP 2025, R&R Theoretical Economics), "Cheap
  Talk in Complex Environments": landscape generalized to Ito
  diffusions INCLUDING OU (Pearson/OU corollary: first-point
  equilibrium exists iff reversion level exceeds bias or a
  stationary-moment condition holds). CORRECTION to the earlier
  claim that OU is unoccupied: OU appears in the tradition in
  ONE-SHOT CHEAP TALK; still absent from multi-shot search. The
  grass paper must cite this and scope its claim: exact multi-shot
  phase diagram on OU remains open. Their complexity index sigma^2/
  |mu| rhymes with our regime analysis.
- BANCHIO & MALLADI (arXiv 2504.19761): fully CLOSED-FORM optimal
  policy -- directional, threshold, index -- but adversarial
  Lipschitz landscape, no prior, endogenous shot count (one or two
  searches when cost is in (1/4,1/2)). The nearest closed-form
  few-shot result; robust, not Bayesian.
- MALLADI (R&R AER) Theorem 1: sequentially optimal = iteratively
  re-solved simultaneous search, worst case is no news.
- HODGSON & LEWIS (Econometrica 2025): GP-landscape consumer search
  estimated on clickstream data; farsighted problem solved
  NUMERICALLY; quote: "each successive outcome determines not only
  whether to stop but where to go next" (S2 p7). Spatial learning
  worth ~13% of welfare.
- LIANG, MU & SYRGKANIS (Econometrica 2022): continuous attention
  over finitely many Gaussian sources; exact deterministic stage-
  switching; farsighted = myopic there.
- ILUT, VALCHEV & VINCENT (Econometrica 2020): ambiguity + GP demand
  curve -> kinks at past prices, price stickiness; noisy repeated
  evaluations, flow payoff.
- GLICK & MYERS (JTP 2015): lab test of the one-observation
  mimic/modify boundary; subjects over-modify under high complexity.
- GROSSE, ZHANG & HENNIG (TMLR 2023, not 2022): optimistic tree
  search on GP samples (Matern/OU covered), asymptotic regret rates,
  budget N grows; no exact small-N solution.

SYNTHESIS (strand D, agent verbatim): exactness is always purchased
by giving something up -- continuous attention or finite-dimensional
Gaussian structure, worst-case robustness in place of a prior,
asymptotic rates in place of finite budgets, or a collapse to one
shot, strategic or behavioral. None solves a small fixed discrete
evaluation budget on a Bayesian random landscape in closed form.
Aybas-Callander's OU corollary and Glick-Myers's tested boundary
confirm that phase boundaries in this tradition are both derivable
and empirically meaningful.
