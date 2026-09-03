# The commitment question, settled
(2026-09-03. Prompted by the k-shot recurrence: does entering a
bracket commit you to it? Answer: no -- provably -- and the true
structure is a threshold rule. Numerics: verify/check_commitment.py.)

## Proposition A (a bad draw sends you back out; naive commitment
## is false)
Let a bracket have end values b, d and let an interior sample reveal
v <= 0 (at or below the process median). Then EVERY placement
interior to the two spoiled sub-brackets, and the revisit of v, is
weakly dominated by exiting to the outside two-shot value
zeta(max(b,d)); strictly if v < 0.

Proof. Consider the sub-bracket with near end b and far end v, an
interior point with correlations (lam2, lam) to its ends,
rho1 = lam2 lam. The conditional mean is mu = A b + B v with
  A = lam2 (1-lam^2)/(1-rho1^2),  B = lam (1-lam2^2)/(1-rho1^2),
both nonnegative, and A <= lam2 because lam >= rho1 implies
1-lam^2 <= 1-rho1^2. Since v <= 0, mu <= lam2 b. The conditional
variance obeys nu = (1-lam2^2)(1-lam^2)/(1-rho1^2) <= 1-lam2^2 by
the same inequality. Hence
  mu + nu/2 <= lam2 b + (1-lam2^2)/2 <= sup_l [ l b + (1-l^2)/2 ]
            = zeta(b),
where the last identification holds for every real b: for b in
[0,1] the supremum is (b^2+1)/2 at l=b; for b>1 it is b at l=1
(since (1+l)/2 <= b); for b<0 it is 1/2 at l=0 (since l b <= 0).
Strictness for v<0: any strictly interior point has B>0, so
mu < lam2 b. The revisit of v pays v <= 0 < 1/2 <= zeta. The same
bound applies to the other sub-bracket with d in place of b. QED

Consequence: the lemma "once inside, stay inside" is FALSE. Entering
a bracket is not a commitment; it is a gamble whose bad outcome is
answered by leaving.

## Proposition B (the value function is monotone in every observed
## value)
For the k-shot game with any frontier of observed (location, value)
pairs, the optimal value is nondecreasing in each observed value.

Proof, by induction on k. Every candidate placement's conditional
mean -- bridge or ray -- is a nonnegative linear combination of
observed values (bridge weights A, B >= 0 as above; ray weight
lam >= 0), and every conditional variance depends on locations only.
Base case k=0: the payoff is a maximum over placements of
mu + nu/2 and over revisits of observed values, each nondecreasing
in each observed value. Step: V_k = max over placements of
E_v[V_{k-1}(frontier + v)]. Raise one observed value; couple the
reveal v' = v + (shift in its conditional mean) >= v; then
V_{k-1} at the shifted state dominates pointwise by the inductive
hypothesis, and the max over placements preserves it. QED

## Corollary (threshold rule at the final shot; measured)
After an interior reveal v with one shot left, the exit menu (rays
and revisits anchored at OUTER values) does not depend on v, while
the stay menu (sub-bracket interiors, revisit v) is nondecreasing in
v by Proposition B. A nondecreasing function crosses a constant
once: stay iff v exceeds a threshold v'(b,d,rho). Measured at
(b,d,rho) = (0.7, 0.7, 0.5): stay iff v > 0.6301 -- NOTABLY BELOW
the anchors: a middle draw somewhat worse than both ends is still
worth staying for, because the sub-bracket keeps one good end and
all of the variance. For k > 1 both menus can depend on v (an exit
may later re-enter), so single crossing is observed numerically but
not claimed as a theorem.

## The corrected recurrence
Exact DP state: the sorted frontier. Tractable relaxation with the
structure above: W_k(b, d, rho; F) = value of k shots restricted to
the current bracket and its descendants, with F the log-value of the
best v-independent fallback (outer zetas and revisits), and
  W_0 = max(F, b, d),
  W_k = sup over split of E_v[ max(W_{k-1}(b,v,.; F'),
        W_{k-1}(v,d,.; F'), F') ],   F' = max(F, v).
This is a LOWER bound on the true adaptive value (it forbids
re-entry after exit and cross-bracket hopping), exact for k <= 2
from any single-bracket state, and threshold-structured by the
corollary. The gap to the exact DP is the price of the freedom
Proposition A proves is sometimes used -- to leave -- and is
measurable on the lattice.

## Round two (2026-09-03, later): the plank closed, k=2 attacked
1. THE SIGMA PARABOLA (proved, in the paper). The symmetric interior
   utility depends on position only through sigma = lam2 + lam,
   becoming a downward parabola on [2 sqrt(rho), 1+rho): the
   pitchfork is the peak entering the range, the exit edge is the
   peak leaving it, the off-middle optimum is U_off =
   (b^2 e^{-2T} + e^{2T})/2, and U_off >= b is literally AM-GM with
   tangency at b = e^{2T}. The b<=1 stretch that had rested on a
   dense grid is now one line, and three elementary no-gap
   inequalities close the middle regime: the revisit-region theorem
   is fully algebraic. Identities checked over 200k random draws
   (verify/check_sigma.py).
2. SINGLE CROSSING AT k=2: SURVIVES (verify/check_crossing_k2.py).
   Stay-minus-exit is monotone through zero exactly once in all
   three probed configs, including asymmetric anchors and a wide
   bracket. Not proved -- the k=1 argument genuinely fails here
   since exits can re-enter -- but the break attempt failed.
3. NEW FINDING: THE STAY THRESHOLD RISES WITH BUDGET. At
   (b,d,rho)=(0.7,0.7,0.5) the reveal must beat ~0.63 to hold a
   single remaining shot inside, but ~1.2 to hold the first of two:
   more remaining shots make the outside option (explore now,
   re-enter later if warranted) more valuable, so the bracket must
   be better to monopolize attention. Conjecture: v-dagger_k is
   increasing in k, saturating at the value where the bracket beats
   even a full fresh exploration program. Open alongside the k-shot
   two-phase conjecture and the pitchfork's inheritance (late-stage
   refinement should hug the running best, not bisect).
