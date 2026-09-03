# The scale-invariant version (Peter's question, 2026-09-03)
Is the search game well defined on a scale-invariant landscape
(Brownian log-height, no mean reversion)? On the infinite line, NO,
for two stacked reasons: (1) BM is a martingale, so a step of
distance D keeps the anchor mean and adds variance D; with the
exponential payoff log-value = d + D/2, increasing forever -- walk
to infinity, value infinite. Mean reversion was the regularizer.
(2) The OU policy's entire content is comparison to sea level, and
scale invariance abolishes sea level: news can only be relatively
good. The OU theory is the broken-symmetry theory (kappa breaks
scale invariance; sea level is the order parameter), and its
boundaries degenerate consistently in the limit: as rho -> 1 the
revisit region's upper edge e^{2 Theta} -> infinity.

Well-defined regularizations:
1. BOUNDED DOMAIN (canonical): ExpBM on [0,1]. Scale-covariant
   family, closed under (t,x) -> (ct, sqrt(c) x) with sigma
   rescaled; sigma^2 T is the one scale-free parameter. Structure
   flips: the Brownian bridge is a martingale so THE SAG DISAPPEARS
   -- interior points keep the linear interpolation of their ends
   plus variance D1 D2/(D1+D2); outside points keep the anchor mean
   plus room-to-the-wall/2. Policy depends only on relative heights
   and remaining room -- no absolute level anywhere. The few-shot
   exact policy here appears open (Grill-Valko-Munos and Calvin are
   many-evaluation asymptotics; Callander is this landscape) and
   would be the natural companion paper: same game, unbroken
   symmetry.
2. TRAVEL COSTS: charge c per unit distance; log-value d + D/2 - cD
   is well-posed iff c > 1/2 -- a sharp phase transition in the
   cost rate. Cute, one derivative from the martingale property.
3. HORIZON / DISCOUNTING: standard, less structural.
Non-fix: relative payoff E[f(t2)/f(t0)] is shift-invariant but the
D/2 divergence survives.
