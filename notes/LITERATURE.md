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

============================================================
## STRAND B: LATER CALLANDER + MANAGEMENT (complete, all full-text)

KEY FACTS:
- GANZ (Org Sci 2020, "Hyperopic Search"): THE nearest antecedent.
  Callander landscape, EXACTLY TWO SHOTS (one offline draw, one
  online placement), TERMINAL-ONLY payoff -- our game minus one shot
  -- but wrapped in a manager-retention agency equilibrium with
  partly computational boundaries. Closed thresholds sqrt(2),
  sigma^2/4. Related: Ganz Org Sci 2018 and 2024. Cite prominently:
  the two-shot hyperopic game is the stepping stone our three-shot
  decision problem completes and exactifies.
- CLM (JPE 2021, "The Power of Referential Advice", read in full
  from Lambert's page): communication game on a drifting Brownian
  path fully known to the expert; ONE receiver placement; the
  good-enough boundary sigma^2/2 mu recurs; referential (interval)
  disclosure dominates bare recommendations by dissuading
  experimentation.
- CALLANDER & MATOUSCHEK (Mgmt Sci 2022): published subtitle is
  "Antitrust Policy" (not "Knowledge Economy" -- fix if cited).
  Hotelling entry with distance-scaled Gaussian quality; one draw;
  spatial Arrow effect; acquisitions suppress novelty.
- CLM (AEJ:Micro forthcoming, "Innovation and Competition on a
  Rugged Technological Landscape"): sequential myopic entrants, one
  placement each, closed-form frontier/niche locations, dead zones
  after breakthroughs, innovation ends inefficiently early.
- CALLANDER & McCARTY (AJPS 2024, "Agenda Control under Policy
  Uncertainty"): Romer-Rosenthal on the Brownian landscape;
  complexity alpha = sigma^2/2|mu|; gridlock interval [0, alpha];
  agenda control suppresses experimentation.
- BARDHI & CALLANDER (WP 2025, "Recombinant Search"): 2-D Brownian
  staple (two drifting BMs + Brownian sheet); myopic short-lived
  researchers; recombination emerges from period 3; frontier search
  advances at most one field at a time.
- ORAIOPOULOS & KAVADIAS (POM 2014): two correlated Gaussian
  domains, one draw per firm, dual-threshold follower policy,
  explore/exploit/forgo.

SYNTHESIS (strand B, agent verbatim): all seven build on the same
primitive but spend their shots inside an equilibrium layer with at
most one or two draws per actor, or let myopic actors take an
open-ended number; the sharp objects are thresholds like
sigma^2/2 mu rather than full phase diagrams. A decision-theoretic
problem with exactly three farsighted draws, terminal-only payoff, a
stationary mean-reverting landscape, and an exact phase diagram sits
in unoccupied territory -- the fixed multi-shot planning problem
this literature repeatedly gestures at (Ganz's two-shot hyperopia
the nearest point) but never solves exactly.

============================================================
## STRAND A: CALLANDER CORE 2008-2019 (complete; six full texts,
## Econometrica 2014 via its published 36pp proof supplement)

- CALLANDER 2008 (QJPS 3(2):123-140): introduces the Brownian policy
  landscape and the first exact complexity threshold -- delegation
  survives iff agency bias <= sigma^2/2mu. Zero search shots; the
  complexity ratio sigma^2/|mu| is born here. Quote p124: higher
  variance / lower drift = "the greater is the complexity of the
  underlying issue."
- CALLANDER 2011 APSR (105(4):643-662): myopic electoral search;
  stay iff status-quo outcome in [-alpha, alpha], alpha =
  sigma^2/2|mu|; monotonic then triangulating phases; STUCK at
  arbitrarily bad outcomes (17-50% in simulation); ~1.5-4 policy
  changes before stability -- an in-model pivot count matching the
  Camuffo field numbers.
- CALLANDER 2011 AER (101(6):2277-2308): the canonical version;
  Prop 6: alpha is ex ante a SUFFICIENT STATISTIC for search
  dynamics (scale invariance) -- the direct ancestor of collapsing a
  phase diagram to dimensionless ratios. Quote p2281: "a bandit
  problem with a continuum of correlated, deterministic arms."
- CALLANDER & HUMMEL 2014 (Econometrica 82(4):1509-1528): TWO-shot
  sequential strategic game; Theorem 1 is a double-cutoff phase
  structure sigma^2/4mu < gamma* < gamma**; preemptive
  experimentation from a status quo that is already ideal. The
  closest precedent for a small-fixed-shot exact phase diagram;
  strategic, flow payoffs.
- CALLANDER & HARSTAD 2015 (QJE 130(2):951-1002): NOT a Brownian
  landscape (preference line, iid binary experiments) -- do not cite
  as landscape work; divergence-to-deter-free-riding, welfare
  maximized at positive heterogeneity.
- CALLANDER & CLARK 2017 (APSR 111(1):184-203): analogical reasoning
  = optimal bridge interpolation; case selection strictly between
  max-error and max-outcome uncertainty; information placement for a
  population, not terminal placement.
- CALLANDER & MATOUSCHEK 2019 (AEJ:Micro 11(1):44-78): risk aversion
  replaces the ideal point; performance trap iff r(m) crosses
  2mu/sigma^2 from above; one-sided unbounded search; divergence
  across fields.

SYNTHESIS (strand A, agent verbatim): the tradition builds one
object -- a fixed realized Brownian path with known (mu, sigma^2)
searched by myopic or two-period actors -- and its signature results
are exact thresholds in sigma^2/|mu| partitioning behavior into
stay/experiment/stuck regimes, with the number of evaluations always
endogenous and payoffs always flow-based. A three-shot terminal-
placement problem on an exponentiated OU landscape differs on all
three structural margins Callander never varies -- fixed shot
budget, terminal objective, mean-reverting landscape -- while
inheriting the phase-boundary aesthetic that Callander-Hummel's
two-cutoff theorem most closely anticipates.

ALL FOUR STRANDS COMPLETE: 29 papers read. Local PDFs cached in the
session scratchpad (see agent reports for filenames).
