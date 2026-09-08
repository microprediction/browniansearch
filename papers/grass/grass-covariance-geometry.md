# Three-evaluation search beyond the OU line

This addendum develops genuine extensions of the opening analysis for *When the Grass Is Greener*. The distinction is between changing coordinates on the same process and changing the set of attainable covariance matrices. All payoffs below are terminal expected `exp(X)`, with a known initial observation, one informative trial, and a terminal recommendation. Fields have mean zero and unit marginal variance.

## 1. The invariant at this budget is three-point covariance geometry

For a centered Gaussian field, the distribution of three evaluated values is determined by their three pairwise correlations. The first trial's reveal law depends on its correlation with the initial point; after that reveal, the terminal decision depends on the set of attainable correlation pairs with those two points.

Thus two fields need not have identical laws, or be coordinate changes of one another, to have identical three-evaluation decision problems. It is sufficient that they have the same available opening correlations and, for each opening correlation, the same feasible terminal correlation pairs.

**Dimension proposition.** Fix a radial covariance function valid on the Euclidean spaces under consideration, and allow unrestricted locations. The three-evaluation problem is identical on every Euclidean space of dimension at least two.

**Reason.** Any three Euclidean points form a triangle that can be realized in a plane. Conversely, all planar triangles can be realized in every higher dimension. A radial kernel converts their edge lengths into exactly the same pairwise correlations. Isotropy makes the direction of the first trial immaterial.

More generally, a budget involving at most H locations, including the initially observed and terminal locations, cannot distinguish Euclidean dimensions at or above H-1 for a common radial Gaussian kernel. Each new location needs only its distances to the previous locations; its component perpendicular to their span can be represented by one new coordinate. The assertion assumes unrestricted domains and an objective and observation model that introduce no dependence on physical direction or coordinates.

## 2. Exact solution of the terminal geometry in dimension at least two

Now take

\[
\operatorname{Cov}(X_s,X_t)=e^{-\|s-t\|},\qquad s,t\in\mathbb R^m,\quad m\ge2.
\]

This is the usual exponential covariance kernel (Matérn smoothness 1/2); its restriction to a line is the OU covariance. See [Rasmussen and Williams, Chapter 4](https://gaussianprocess.org/gpml/chapters/RW4.pdf) for the covariance family. The full spatial field has additional geometry beyond the line.

Suppose the observed log-values are b,d and their correlation is rho. Let x,y be a terminal point's correlations to the two observations. Its distances to them are -log x and -log y. Therefore the three triangle inequalities give the exact feasible region

\[
\boxed{\mathcal C_\rho=
\{(x,y)>0:xy\le\rho,\;x\ge\rho y,\;y\ge\rho x\}.}
\]

Use its compact closure when allowing limiting independent points. The inequalities imply x,y<=1. Every pair in this region is realizable by a Euclidean triangle.

The log of conditional expected terminal payoff is

\[
L(x,y)=\frac12+
\frac{(b-\rho d)x+(d-\rho b)y
-\tfrac12(x^2-2\rho xy+y^2)}{1-\rho^2}.
\]

It is a strictly concave quadratic on the ambient correlation plane. Its unique unconstrained stationary point is

\[
\boxed{(x,y)=(b,d).}
\]

The boundary of the feasible region consists precisely of the original OU line placements: xy=rho is the bracket; x=rho y and y=rho x are the two exterior rays. Although the feasible region is not convex, an interior maximum must be the unique unconstrained stationary point. Hence the exact terminal theorem is

\[
\boxed{
V_m(b,d,\rho)=\max\{V_1(b,d,\rho),L_{\rm free}(b,d,\rho)\},
}
\]

where the second candidate is included only if (b,d) belongs to the feasible region, and

\[
L_{\rm free}=\frac12+
\frac{b^2-2\rho bd+d^2}{2(1-\rho^2)}.
\]

This adds just one explicit candidate to the paper's algebraic terminal solution. The opening still needs only a scalar Gaussian expectation and optimization over rho. The solution is exact in every dimension m>=2.

An additional exact consequence: if either observed value is at least one, the unconstrained stationary point cannot lie strictly inside the feasible region. In that case the planar/higher-dimensional terminal value equals the one-dimensional OU value. In particular, the entire opening objective is exactly identical in all Euclidean dimensions for initial b>=1.

## 3. A Lambert-W opening coefficient

For small positive b, write rho=kb and p=1/sqrt(2pi). For a fixed reveal 0<d<1, the limiting terminal correlation to the revealed point is y=d. Write x=bu. The feasible range becomes

\[
kd\le u\le k/d.
\]

The leading uplift over the trial-attached exterior value is

\[
\frac{b^2}{2}\{(1-kd)^2-(u-1)^2\}.
\]

For 0<k<1, choose u=1 if d<k, and u=k/d if d>k. The first branch is genuinely off the line through the anchors; the second is the existing bracket solution.

Integrating the leading improvement gives

\[
H_m(k)=\int_0^k\frac{(1-kd)^2}{2}\,\mathrm d d
+\int_k^1\left[k(d^{-1}-d)-\frac{k^2}{2}(d^{-2}-d^2)\right]\,\mathrm d d
=-k\log k-\frac k2+\frac{2k^2}{3}.
\]

After adding the Gaussian reveal-distribution perturbation and the incumbent contribution, the polynomials simplify:

\[
e^{-1/2}J_m(b,kb)=1+p+b^2Q_m(k)+O(b^4),
\]

\[
\boxed{Q_m(k)=\frac14+\frac k2-\frac{k^2}{4}-pk\log k,
\qquad 0<k\le1.}
\]

For k>=1 the expression is

\[
Q_m(k)=\frac14+\frac{1+p}{2}k
-\left(\frac14+\frac{2p}{3}\right)k^2+\frac{p}{6k},
\]

and is strictly decreasing there. On (0,1),

\[
Q_m'(k)=\frac{1-k}{2}-p(\log k+1),\qquad
Q_m''(k)=-\frac12-\frac pk<0.
\]

Set c=1/(2p)=sqrt(pi/2). The unique maximizing root satisfies

\[
\log k=c(1-k)-1,
\qquad (ck)e^{ck}=ce^{c-1}.
\]

Therefore, with W_0 denoting the principal Lambert W branch,

\[
\boxed{
\rho_m^*(b)=\kappa_{\ge2}b+O(b^3),\qquad
\kappa_{\ge2}=\frac{W_0(ce^{c-1})}{c}
=0.6041696557198694\ldots .
}
\]

The one-dimensional coefficient remains 0.540062023872735.... The new coefficient describes a different feasible terminal geometry; it is not a reinterpretation or correction of the line result.

### Localization and the remainder

The same regression estimate used on the line applies because x>=rho y. Put u=(x-rho y)/(1-rho^2)>=0 and decompose

\[
L=dy+\frac{1-y^2}{2}+(b-\rho d)u-\frac{1-\rho^2}{2}u^2.
\]

For d>=0 the final two terms are at most b^2/[2(1-rho^2)]. For d<0, symmetric regression on the incumbent bounds every terminal point by its two-shot ray value. The strict convex-order loss at b=0 and the resulting local bound J<=J_0+Cb^2+Cb rho-c rho^2 force rho*=O(b). The uniquely maximizing Q_m then localizes rho*/b near kappa_ge2.

For k in a compact neighborhood of this root and b small, the exact terminal branches are:

| Reveal d | Terminal branch |
|---|---|
| d <= k b^2 | Incumbent's optimal exterior ray |
| k b^2 < d <= k | Free correlation optimum (x,y)=(b,d) |
| k < d < d_s | Bracket optimum |
| d >= d_s | Revealed trial itself |

Here

\[
d_s=\frac{1-k^2b^2+2kb^2}{1+k^2b^2}.
\]

In t=b^2 all endpoints, reveal-density parameters, and branch formulas are analytic. The bracket optimizer is analytic by the implicit function theorem for d>=k>0. Integrating piecewise gives an expansion in t, including after differentiating in k. Strict negativity of Q_m'' then yields k*(b)=kappa_ge2+O(b^2), establishing the O(b^3) policy remainder. Unlike the line objective, this objective has no cubic-in-b value term: the small-reveal crossover is at d=k b^2 instead of d=b.

### Numerical verification

The supplied verification script compares the exact line boundary maximum with the feasible free candidate, integrates analytic envelope derivatives, and solves the opening first-order condition.

| b | Direct optimal rho/b |
|---:|---:|
| 0.1 | 0.603598238072 |
| 0.01 | 0.604163937224 |
| 0.001 | 0.604169598534 |
| 0.0003 | 0.604169650573 |
| Lambert W limit | 0.604169655720 |

The numerically inferred cubic coefficient is about -0.0571853972; unlike the leading coefficient, it has not been separately reduced to an analytic formula in this addendum.

## 4. Genuine kernel universality at high incumbents

Let X be any centered unit-variance Gaussian field with positive correlations R(s,t). Suppose

\[
d(s,t)=-\log R(s,t)
\]

is a metric, or a pseudometric after identifying equivalent points. No stationarity, Euclidean indexing, or Markov assumption is required.

For initial b>=1 and a trial whose correlation is rho, the exact bounds are

\[
\boxed{
\mathbb E e^{\max(b,D)}\le J_X(b,\text{trial})\le J_{\rm OU}(b,\rho),
\quad D\sim N(b\rho,1-\rho^2).
}
\]

The lower bound simply chooses the better observed point. For the upper bound, the metric triangle inequalities put every actual terminal correlation pair in C_rho. Since b>=1 excludes an interior stationary maximum, the maximum over this entire region lies on its OU-line boundary. An actual field may realize only part of the region, so its value cannot exceed that boundary maximum.

The prior high-b calculation on the line established the uniform estimate

\[
0\le e^{-b}\left[J_{\rm OU}(b,\rho)-\mathbb E e^{\max(b,D)}\right]
\le Cb^{-3},\qquad 0\le\rho\le1.
\]

Consequently that same uniform estimate applies to J_X. Assume opening correlations in an interval (rho_0,1) are attainable. Then every optimal opening, or any opening with value within o(e^b/b) of optimum, satisfies

\[
\boxed{b^2[1-R(o,t_b^*)]\longrightarrow
c_\infty=0.749095787016391\ldots,}
\]

and

\[
\boxed{\log J_X^*(b)=b+
\frac{0.202456490188025\ldots}{b}+o(b^{-1}).}
\]

For completeness, putting rho=1-c/b^2 gives the leading observed-anchor profile

\[
H(c)=\mathbb E(\sqrt{2c}Z-c)_+
=\sqrt{2c}\,\phi(\sqrt{c/2})-c\Phi(-\sqrt{c/2}).
\]

Its unique maximum occurs at c_infty=2a_infty^2, where phi(a_infty)=2a_infty Phi(-a_infty). The Gaussian tail bound from the line calculation excludes c tending to zero or infinity for any asymptotically optimal sequence. Uniform convergence of the profile on compact c-ranges and the uniform O(b^-3) squeeze transfer both the value and optimizer limits to the entire metric-correlation class.

### Examples beyond OU

* Powered-exponential fields R(s,t)=exp(-lambda ||s-t||^alpha), 0<alpha<=1, in every Euclidean dimension. For alpha<1 these are not time changes of the stationary OU line: their three-point distances do not obey the OU multiplicative equality along straight segments.
* Nontrivial mixtures R(s,t)=E exp(-Lambda ||s-t||), Lambda>0. These are generally not Markov along a line. The function g(u)=-log E exp(-Lambda u) is increasing and concave with g(0)=0, hence subadditive. Therefore g(||s-t||) is a metric, and the theorem applies.

If locally 1-R(o,t) is asymptotic to a||t-o||^alpha, the corresponding physical distance satisfies

\[
\|t_b^*-o\|\sim
\left(\frac{c_\infty}{a b^2}\right)^{1/\alpha}.
\]

The coefficient in correlation coordinates is universal in this class; the distance exponent is allowed to change.

## 5. Interpretation

The small-incumbent coefficient detects the set of possible terminal correlations: line geometry gives 0.540062..., while every Euclidean dimension at least two gives the Lambert-W value 0.604169.... The entire three-evaluation policy is already insensitive to further increases in dimension.

The high-incumbent constants have wider universality: the logarithmic correlation need only satisfy triangle inequalities. This covers different covariance kernels and non-Markov fields, and follows from an exact comparison rather than a deterministic coordinate change.

These are new derivations in this conversation. The covariance family and elementary triangle embedding are standard; no claim is made that the resulting search theorems or coefficient formulas have been exhaustively checked against the literature.
