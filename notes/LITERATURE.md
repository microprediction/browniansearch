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
