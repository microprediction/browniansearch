# Analytic opening limits for *When the Grass Is Greener*

Derived from the supplied September 5, 2026 version of `grass-compact.pdf`.

## Main result

For the unit-scale model in the paper, the optimal opening correlation satisfies

\[
\boxed{\rho^*(b)=\kappa_0 b+O(b^3),\qquad b\downarrow0,}
\]

where

\[
\boxed{\kappa_0=0.540062023872735\ldots .}
\]

Thus the conjectured asymptotic form is correct, but the coefficient is **not**
\(1/\sqrt\pi=0.564189583547756\ldots\). The coefficient has an exact characterization by one elementary transcendental equation. This is an analytic characterization, not an elementary closed-form evaluation.

The subscript distinguishes this constant from the OU correlation-decay parameter, also called \(\kappa\) in the paper. In the discussion of physical distances below, that decay parameter is denoted \(\ell\).

Put \(p=\phi(0)=1/\sqrt{2\pi}\). Let \(a_0\) be the unique root in \((0,1)\) of

\[
\boxed{
(1+a^2)\log a+2-\frac{a^2}{2}+\frac{a^4}{6}
-\sqrt{\frac\pi2}(1-a)^2=0.
}
\]

Then

\[
a_0=0.293252947509029\ldots,
\qquad \kappa_0=\frac{2a_0}{1+a_0^2}.
\]

An additional expansion, derived in Appendix A, is

\[
\rho^*(b)=0.540062023872735\,b
-1.06803546749435\,b^3+O(b^4).
\]

The leading theorem does not require this fourth-order value calculation.

## 1. Objective and scaling

Use expected payoff, rather than its logarithm:

\[
J(b,\rho)=\mathbb E\exp V(b,D,\rho),
\qquad D\sim N(b\rho,1-\rho^2).
\]

This has the same optimizer as the log-value used in the paper. Let

\[
\zeta(d)=
\begin{cases}
1/2,&d\le0,\\
(1+d^2)/2,&0<d<1,\\
d,&d\ge1.
\end{cases}
\]

At \(b=\rho=0\), Proposition 3 gives

\[
J_0=e^{1/2}(1+p),\qquad W_0=\log J_0.
\]

Set \(\rho=kb\). The expansion to optimize is

\[
\boxed{
e^{-1/2}J(b,kb)=1+p+b^2Q(k)+\frac p3b^3+O(b^4).
}
\tag{1}
\]

The remainder and its first derivative in \(k\) are uniform on compact neighborhoods of the eventual optimizer. The cubic term is independent of \(k\); this is why the opening has no \(b^2\) term.

## 2. The interior option survives at leading order

Let \(y\) denote the terminal location's correlation to the second observation \(d\). Its correlation to the incumbent is \(\rho/y\). The bridge log-payoff is

\[
L(y)=\frac{
dy+b\rho/y-b\rho y-\rho^2d/y
+\tfrac12(1+\rho^2-y^2-\rho^2/y^2)
}{1-\rho^2}.
\]

For fixed \(0<d<1\), the limiting optimum attached to \(d\) is \(y=d\). Substituting \(\rho=kb\) and using the envelope theorem gives

\[
\sup_y L(y)=\zeta(d)+b^2 f(d,k)+O(b^4),
\]

where

\[
f(d,k)=k(d^{-1}-d)-\frac{k^2}{2}(d^{-2}-d^2).
\tag{2}
\]

The exterior alternative remains available. Therefore the leading interior uplift is \(b^2[f(d,k)]_+\), not \(b^2f(d,k)\).

For \(0<k<1\),

\[
f(d,k)>0
\iff k<\frac{2d}{1+d^2}
\iff d>a(k),
\qquad
a(k)=\frac{k}{1+\sqrt{1-k^2}}.
\tag{3}
\]

For \(k\ge1\), there is no positive leading interior uplift. At the optimum, the limiting active interval is \(a_0<d<1\). Its lower edge stays near 0.2933 even though the incumbent tends to zero. Ignoring this switch loses the correct coefficient.

Because

\[
e^{\zeta(d)}\phi(d)=e^{1/2}p,\qquad 0<d<1,
\]

the leading interior contribution has an elementary integral:

\[
H(k)=\int_{a(k)}^1 f(d,k)\,dd
=k\left[-\log a-\frac{1-a^2}{2}\right]
-\frac{k^2}{2}\left[\frac1a-\frac43+\frac{a^3}{3}\right].
\tag{4}
\]

## 3. Exterior contribution and the scalar optimization

Expanding the density of \(D\) gives

\[
\frac{f_D(d)}{\phi(d)}
=1+b^2\left[kd+\frac{k^2}{2}(1-d^2)\right]+O(b^4).
\]

For \(h(d)=e^{\zeta(d)}\), elementary Gaussian integrations yield

\[
e^{-1/2}\mathbb E[Zh(Z)]=\frac{1+p}{2},
\qquad
e^{-1/2}\mathbb E[(Z^2-1)h(Z)]=\frac12+\frac{4p}{3}.
\]

Retaining the incumbent, when preferable, adds

\[
e^{1/2}\left(\frac{b^2}{4}+\frac p3b^3+O(b^4)\right).
\]

Combining these terms with (4),

\[
\boxed{
Q(k)=\frac14+\frac{1+p}{2}k
-\left(\frac14+\frac{2p}{3}\right)k^2+pH(k),\quad 0<k<1.
}
\tag{5}
\]

Use \(H(0)=0\) and \(H(k)=0\) for \(k\ge1\).

Since the integrand in (4) vanishes at its lower endpoint, differentiation gives

\[
Q'(k)=\frac{1-k}{2}
+p\left[-\log a+\frac{a^2}{2}-\frac{k}{a}-\frac{ka^3}{3}\right].
\tag{6}
\]

Substitution of \(k=2a/(1+a^2)\) gives the boxed scalar equation above.

This critical point is the unique global maximizer of \(Q\). Indeed,

\[
\boxed{
Q''(k)=-\frac12+p\left(-\frac{1}{2a}+a+\frac{a^3}{6}\right)<0,
\quad 0<k<1.
}
\]

The parenthesis is increasing in \(a\) and bounded above by \(2/3\), while \(2p/3<1/2\). Also \(Q'(0+)=+\infty\), \(Q'(1-)=-5p/6<0\), and the quadratic branch for \(k\ge1\) is decreasing. This proves uniqueness of the scalar root as well as of the limiting slope.

## 4. Why this is a theorem about the optimizer

There are two points beyond a formal expansion.

**Localization.** At \(b=0\), strict convex ordering gives \(J(0,\rho)<J_0\) for every \(\rho>0\). Couple the second observation at incumbent \(b\) with that at incumbent zero by adding \(b\rho\). Every terminal conditional mean increases by \(b\operatorname{Corr}(X_t,X_0)\in[0,b]\). Consequently \(J(b,\rho)\le e^bJ(0,\rho)\), which first implies \(\rho^*(b)\to0\).

A sharper estimate yields \(\rho^*(b)=O(b)\). For a bridge point with correlations \(x\) to the incumbent and \(y\) to the second observation, put

\[
t=\frac{x-\rho y}{1-\rho^2}\ge0.
\]

Its log-payoff has the exact regression decomposition

\[
L=dy+\frac{1-y^2}{2}+(b-\rho d)t-\frac{1-\rho^2}{2}t^2.
\]

For \(d\ge0\), the last two terms are at most \(b^2/[2(1-\rho^2)]\). For \(d<0\), abandonment gives the same overall bound using the incumbent. Thus

\[
J(b,\rho)\le
\exp\left(\frac{b^2}{2(1-\rho^2)}\right)\mathbb E h(D)
\le J_0+C b^2+C b\rho-c\rho^2
\]

locally, for fixed positive constants \(C,c\). Comparing with \(J(b,0)\ge J_0\) proves \(\rho^*=O(b)\). The leading expansion is uniform on bounded \(k\)-ranges, with continuity at zero obtained by splitting the \(d\)-integral near zero. Strict maximization of \(Q\) then implies \(\rho^*/b\to\kappa_0\).

**Remainder after differentiation.** Near \(k=\kappa_0\), the active bridge region is bounded away from \(d=0\). Its lower edge is a simple crossing at \(a(k)+O(b^2)\). Its upper stopping edge is

\[
d_s=\frac{1-\rho^2+2\rho b}{1+\rho^2}
=1+2k(1-k)b^2+O(b^4).
\]

The sliver above \(d=1\) has width \(O(b^2)\) and gain \(O(b^4)\), so does not alter (1). All bridge and Gaussian-density expansions away from the incumbent cutoff depend smoothly on \(b^2\).

The nonsymmetric \(b^3\) term comes from the small interval \(0<d<b\), where retaining the incumbent wins. Its coefficient \(p/3\) is independent of \(k\). Therefore (1) holds with its first \(k\)-derivative, and

\[
0=\partial_k J(b,k^*(b)b)
=e^{1/2}b^2\{Q'(k^*(b))+O(b^2)\}.
\]

Since \(Q''(\kappa_0)<0\), it follows that \(k^*(b)=\kappa_0+O(b^2)\), proving the claimed \(O(b^3)\) remainder for \(\rho^*\). This argument does not assume an odd symmetry across \(b=0\); on the negative side the optimum remains exactly zero.

## 5. Consequences and numerical checks

The optimized log-value has the expansion

\[
\boxed{
\log J(b,\rho^*(b))
=W_0+0.372994794891796\,b^2
+0.095058074944773\,b^3+O(b^4).
}
\]

Here \(Q(\kappa_0)=0.521798188943793\ldots\). The value is continuously differentiable through \(b=0\), but its second derivative changes from zero on the negative side to \(0.745989589783591\ldots\) on the positive side.

If interior terminal placements are excluded, the \(H\) term disappears. The corresponding opening coefficient **does** have a simple closed form:

\[
\boxed{
\rho^*_{\rm ext}(b)=\frac{1+p}{1+8p/3}\,b+O(b^3)
=0.677832660697169\,b+O(b^3).
}
\]

Thus interior placement affects the opening slope at leading order even though its value premium tends to zero. Relative to the two-shot rule \(\rho=b\), the optimal three-shot trial travels asymptotically an additional \(-\log\kappa_0=0.616071286996\ldots\) correlation lengths:

\[
t_1^*(b)=\frac{-\log b-\log\kappa_0}{\ell}+O(b^2),
\qquad \rho=e^{-\ell t_1}.
\]

The direct numerical calculation uses the exact bridge optimum, adaptive quadrature split at branch crossings, and the analytic derivative of the expectation. This avoids estimating the optimizer by subtracting nearly equal objective values.

| \(b\) | Direct \(\rho^*(b)/b\) |
|---:|---:|
| 0.1 | 0.530935356412 |
| 0.03 | 0.539119018649 |
| 0.01 | 0.539955498316 |
| 0.003 | 0.540052415092 |
| 0.001 | 0.540060955913 |
| 0.0003 | 0.540061927743 |
| Analytic limit | 0.540062023873 |

In particular, the paper's tabulated \(\rho^*\approx0.053\) at \(b=0.1\) is consistent with this result. The slope inferred at moderate \(b\) is not its limit at zero.

All constants here concern the paper's normalization \(s=1\). A different payoff/path scale changes the opening expectation and needs its own expansion; the universal terminal phase diagram alone does not make this opening coefficient universal in \(b/s\).


## Appendix A. Next term in the optimal opening

Write \(p=(2\pi)^{-1/2}\), \(\rho=kb\), \(t=b^2\), and
\[
a=a(k)=\frac{k}{1+\sqrt{1-k^2}},\qquad 0<k<1.
\]
Let \(J(b,\rho)=\mathbb E[e^{V(b,D,\rho)}]\) denote expected payoff, before taking its logarithm. Locally uniformly for \(k\) near the maximizing coefficient,
\[
e^{-1/2}J(b,kb)
=1+p+b^2Q(k)+\frac p3 b^3+b^4S(k)+O(b^5),\qquad b\downarrow0.
\]
The expansion also holds after one derivative in \(k\). The cubic term in the value is independent of \(k\), which explains why the optimal correlation has no quadratic term.

Define, for \(a<d<1\),
\[
\begin{aligned}
f(d,k)&=k(d^{-1}-d)-\frac{k^2}{2}(d^{-2}-d^2),\\
q(d,k)&=k(1+d^{-2})(k/d-1),\\
A(d,k)&=kd+\frac{k^2}{2}(1-d^2),\\
H(d,k)&=k^2f+\frac12q^2+\frac12f^2+Af.
\end{aligned}
\]
An exact elementary integral for the fourth-order coefficient is
\[
\boxed{S(k)=S_{\rm ext}(k)+p\int_{a(k)}^1 H(d,k)\,\mathrm d d,}
\]
where
\[
S_{\rm ext}(k)=\frac1{16}-\frac p2k
+\left(\frac14+\frac{2p}{3}\right)k^2
-\left(\frac14+\frac{7p}{8}\right)k^3
+\left(\frac1{16}+\frac{3p}{20}\right)k^4.
\]
Every term of \(H\) is a Laurent monomial in \(d\), so the integral involves only rational functions and \(\log a\).

At the unique maximizing root \(k_0=0.5400620238727354\ldots\),
\[
Q''(k_0)=-1.061533837111570\ldots,\qquad
S'(k_0)=-1.133755787980532\ldots.
\]
Consequently,
\[
\boxed{\rho^*(b)=0.5400620238727354\ldots\,b
-1.068035467494355\ldots\,b^3+O(b^4).}
\]
Here the cubic coefficient is exactly \(-S'(k_0)/Q''(k_0)\).

### Derivation

Orient the bridge so that \(y\) is the correlation with the revealed value \(d\). Its log-payoff is exactly
\[
L(y)=\frac{dy+(1-y^2)/2+tN_1(y)}{1-k^2t},
\]
where
\[
N_1(y)=k(y^{-1}-y)-k^2d/y-\frac{k^2}{2}(y^{-2}-1).
\]
Thus \(L=L_0+tL_1+t^2k^2L_1+O(t^3)\), with \(L_0(y)=dy+(1-y^2)/2\). Since \(L_0\) has its maximum at \(y=d\), with second derivative \(-1\),
\[
L_1(d)=f(d,k),\qquad L_1'(d)=q(d,k).
\]
The optimized bridge value therefore satisfies
\[
L_* =\frac{1+d^2}{2}+tf+t^2\left(k^2f+\frac{q^2}{2}\right)+O(t^3).
\]
The reveal density, relative to the standard normal density, equals \(1+tA+O(t^2)\). Expanding the exponential of the bridge improvement gives \(H\) above. The bridge beats the exterior option at leading order precisely on \(a(k)<d<1\). Its lower boundary moves by \(O(t)\); because \(f(a,k)=0\), that motion changes the value only at order \(t^3=b^6\). The narrow extension above \(d=1\) also contributes only at order \(b^6\).

For the exterior baseline, put \(F(d)=e^{\zeta(d)-1/2}\). Distributional Gaussian integration by parts gives
\[
\begin{aligned}
\mathbb EF''(Z)&=\tfrac12+\tfrac43p,\\
\mathbb EF'''(Z)&=\tfrac12+\tfrac74p,\\
\mathbb EF''''(Z)&=\tfrac12+\tfrac65p.
\end{aligned}
\]
Expanding the expectation under \(D\sim N(kt,1-k^2t)\), its \(t^2\) coefficient is
\[
\frac{k^2}{2}\mathbb EF''(Z)-\frac{k^3}{2}\mathbb EF'''(Z)
+\frac{k^4}{8}\mathbb EF''''(Z).
\]
Replacing \(F(d)\) by the incumbent payoff \(e^{t/2}\) for \(d<b\) adds
\[
\frac14b^2+\frac p3b^3+
\left(\frac1{16}-\frac{pk}{2}\right)b^4+O(b^5),
\]
which yields \(S_{\rm ext}\).

To differentiate \(S\), include the moving lower endpoint:
\[
S'(k)=S_{\rm ext}'(k)+p\left[\int_a^1\partial_kH(d,k)\,\mathrm d d-H(a,k)a'(k)\right],
\]
where
\[
a'(k)=\frac{(1+a^2)^2}{2(1-a^2)},\qquad H(a,k)=\frac12q(a,k)^2>0.
\]
Unlike the corresponding first derivative of \(Q\), this boundary term does not vanish.

### Optional fifth-order value term

The bridge contribution is analytic in \(t=b^2\) near the relevant regime. The next odd power comes from the exterior incumbent crossover \(0<d<b\):
\[
e^{-1/2}J(b,kb)=1+p+b^2Q(k)+\frac p3b^3+b^4S(k)
+p\left(\frac1{15}+\frac{k^2}{6}\right)b^5+O(b^6).
\]
Accordingly, retaining one more term gives
\[
\rho^*(b)=k_0b-1.068035467494355\ldots\,b^3
+0.0676547990683150\ldots\,b^4+O(b^5),
\]
with exact quartic coefficient \(-pk_0/(3Q''(k_0))\). Thus an odd-power-only expansion beyond the cubic term would be incorrect.


## Appendix B. Additional analytic limits of the opening policy

Write
\[
J(b,\rho)=\mathbb E\exp V(b,D,\rho),\qquad
D\sim N(b\rho,1-\rho^2),\qquad g(x)=e^{\zeta(x)}.
\]
The paper reports \(\log J\); maximizing either quantity gives the same opening correlation. Here \(\phi,\Phi\) denote the standard normal density and distribution function, and \(\bar\Phi=1-\Phi\).

### B.1. Exact opening curve at the median

Abandonment removes the interior option at \(b=0\), so \(J(0,\rho)=\mathbb E g(\sqrt{1-\rho^2}Z)\). Splitting the Gaussian integral at zero and one gives, for \(0<\rho<1\),
\[
\boxed{
J(0,\rho)=\frac{e^{1/2}}2
 +\frac{e^{1/2}}{2\rho}
 \operatorname{erf}\!\left(\frac{\rho}{\sqrt{2(1-\rho^2)}}\right)
 +e^{(1-\rho^2)/2}
 \Phi\!\left(-\frac{\rho^2}{\sqrt{1-\rho^2}}\right).
}
\]
Both endpoint singularities are removable. The values are
\[
J(0,0)=e^{1/2}\left(1+\frac1{\sqrt{2\pi}}\right),
\qquad J(0,1)=e^{1/2}.
\]
The expansions are
\[
J(0,\rho)=e^{1/2}\left(1+\frac1{\sqrt{2\pi}}\right)
-e^{1/2}\left(\frac14+\frac{2}{3\sqrt{2\pi}}\right)\rho^2
+O(\rho^4),\qquad \rho\downarrow0,
\]
and
\[
J(0,\rho)=e^{1/2}\left[1+\frac{1-\rho}{2}
+O((1-\rho)^2)\right],\qquad \rho\uparrow1.
\]
For the first expansion, the variance differentiation identity gives the quadratic coefficient as \(-\tfrac12\mathbb E g''(Z)\), where
\(\mathbb E g''(Z)=e^{1/2}[\tfrac12+4/(3\sqrt{2\pi})]\).

### B.2. Every positive incumbent has an interior optimal correlation

**Proposition.** For every fixed \(b>0\), every globally optimal opening correlation lies in \((0,1)\).

Here “interior” refers to the opening correlation, not the terminal placement. To prove the proposition, it suffices to rule out both endpoints.

Put \(c_0=e^{1/2}/\sqrt{2\pi}\). The right derivative at the fresh-draw endpoint is
\[
\boxed{
\partial_\rho J(b,0+)=
\begin{cases}
c_0\!\left[(b^{-1}-b)(e^{b^2/2}-1)-b\log b\right]
+\tfrac b2e^{1/2},&0<b<1,\\[2mm]
b e^{1/2}\Phi(1-b),&b\ge1.
\end{cases}}
\]
It is strictly positive. In particular, opening completely independently is suboptimal for every positive initial observation, however small.

For completeness, the value at that endpoint is
\[
J(b,0)=
\begin{cases}
g(b)\Phi(b)+c_0(1-b)+e^{1/2}/2,&0<b<1,\\
e^b\Phi(b)+e^{1/2}\Phi(1-b),&b\ge1.
\end{cases}
\]
To obtain the derivative when \(b<1\), separate the change in the distribution of \(D\) from the newly available bridge premium. The distributional contribution is
\[
b\left[c_0\frac{1-b^2}{2}+\frac{e^{1/2}}2\right].
\]
For \(0<d<b\), the first bridge correction to the log-value is
\(\rho d(b^{-1}-b)\). For \(b<d<1\), it is
\(\rho b(d^{-1}-d)\). Integrating these corrections gives respectively
\[
c_0(b^{-1}-b)(e^{b^2/2}-1),\qquad
c_0b\left[-\log b-\frac{1-b^2}{2}\right].
\]
Adding cancels the polynomial terms. For \(b\ge1\), bridge corrections have zero first derivative and only the distributional term remains. The logarithm in this fixed-\(b\) derivative also warns against taking its \(b\downarrow0\) limit as a uniform joint expansion.

At the other endpoint, set \(\varepsilon=1-\rho\). For fixed \(0<b<1\),
\[
\boxed{
J(b,1-\varepsilon)=g(b)
\left[1+b\sqrt{\frac{\varepsilon}{\pi}}
+\frac{\varepsilon}{2}+O(\varepsilon^{3/2})\right].}
\]
For fixed \(b\ge1\),
\[
\boxed{
J(b,1-\varepsilon)=e^b
\left[1+\sqrt{\frac{\varepsilon}{\pi}}
+\frac{1-b}{2}\varepsilon+O(\varepsilon^{3/2})\right].}
\]
Indeed, \(\Delta=D-b=-b\varepsilon+\sqrt{2\varepsilon-\varepsilon^2}Z\), and Taylor expansion of \(g(b+\Delta_+)\) gives these coefficients. For fixed \(b<1\), the bridge cannot close the positive log-value gap \((1-b)^2/2\) except on exponentially unlikely observations. For \(b\ge1\), a bridge improvement requires \(\Delta=O(\varepsilon)\); its probability is \(O(\sqrt\varepsilon)\) and its gain is \(O(\varepsilon)\), so it first contributes at order \(\varepsilon^{3/2}\). At \(b=1\), the selected positive increments use the right-hand second derivative \(g''(1+)=e\), giving a zero coefficient of \(\varepsilon\). The positive square-root terms exclude \(\rho=1\). Continuity on the compactified interval supplies a maximizer.

### B.3. High-incumbent opening law

**Theorem.** Let \(\rho_*(b)\) be any maximizing opening correlation. As \(b\to\infty\),
\[
\boxed{b^2(1-\rho_*(b))\longrightarrow c_\infty
=0.7490957870163905\ldots,}
\]
and
\[
\boxed{\log\max_\rho J(b,\rho)
=b+\frac{A_\infty}{b}+o(b^{-1}),\qquad
A_\infty=0.2024564901880247\ldots.}
\]
The constants are characterized by the unique positive solution
\[
\phi(a_\infty)=2a_\infty \bar\Phi(a_\infty),\qquad
a_\infty=0.612003180962481\ldots,
\]
with \(c_\infty=2a_\infty^2\) and
\(A_\infty=c_\infty \bar\Phi(a_\infty)\).
Thus the optimal physical opening distance is asymptotic to
\(c_\infty/(\kappa_{\rm OU}b^2)\), where \(\kappa_{\rm OU}\) is the OU decay rate.

**Proof.** For \(b\ge1\), the exterior-only terminal reward is exactly \(e^{\max(b,D)}\). Set \(\varepsilon=1-\rho\) and
\[
H_b(\varepsilon)=\mathbb E(e^\Delta-1)_+,
\qquad \Delta\sim N(-b\varepsilon,\varepsilon(2-\varepsilon)).
\]
First, uniformly over all opening correlations,
\[
\frac{J(b,\rho)}{e^b}=1+H_b(\varepsilon)+O(b^{-3}). \tag{A}
\]
Here is a useful proof of the uniform error. The unequal-anchor stopping criterion shows that a bridge improvement is impossible if \(b\ge(1+\rho)/(1-\rho)\). Otherwise \(\varepsilon<2/(b+1)\), and that same criterion bounds the improving observations by \(|\Delta|\le2\varepsilon\), for all sufficiently large \(b\). The bridge mean is at most the larger anchor, while its variance is at most \(\varepsilon/(2-\varepsilon)\); consequently its excess payoff, divided by \(e^b\), is at most \(C\varepsilon\) on this event. Gaussian density bounds give
\[
\Pr\{|\Delta|\le2\varepsilon\}
\le C\sqrt\varepsilon\exp(-b^2\varepsilon/16).
\]
The expected excess is therefore bounded by
\(C\varepsilon^{3/2}\exp(-b^2\varepsilon/16)\le C'b^{-3}\), proving (A).

Now set \(\varepsilon=c/b^2\). Uniformly for \(c\) in compact positive intervals,
\[
bH_b(c/b^2)\longrightarrow
A(c)=\mathbb E(-c+\sqrt{2c}Z)_+
=\sqrt{2c}\,\phi(\sqrt{c/2})-c\bar\Phi(\sqrt{c/2}).
\]
No maximizing sequence escapes this scale: exponential tilting and
\((e^x-1)_+\le e^x x_+\) give
\[
bH_b(\varepsilon)
\le\sqrt{2x}\,\phi\!\left((1-2/b)\sqrt{x/2}\right),
\qquad x=b^2\varepsilon.
\]
This upper bound vanishes if \(x\to0\) or \(x\to\infty\), whereas \(A(c)>0\) at any fixed positive \(c\). Finally,
\[
A'(c)=\frac{\phi(\sqrt{c/2})}{\sqrt{2c}}-\bar\Phi(\sqrt{c/2}).
\]
The maximizing equation is the stated equation for \(a_\infty\). Uniqueness follows because \(a\bar\Phi(a)/\phi(a)\) increases strictly from zero to one: after substituting \(t=au\), it equals
\(\int_0^\infty e^{-t-t^2/(2a^2)}\,dt\). Compactness and uniform convergence complete the proof.

#### Optional refinement: the disappearing interior premium

The same local analysis gives, for fixed \(c>0\),
\[
\boxed{
\frac{J_{\rm full}(b,1-c/b^2)-J_{\rm rays}(b,1-c/b^2)}{e^b}
\sim\frac{c^{3/2}e^{-c/4}}{12\sqrt\pi\,b^3}.}
\]
To see the coefficient, set \(\Delta=\varepsilon y\) and parametrize the short bracket by its fractional distance \(q\). The leading bridge log-value above \(b\) is
\(\varepsilon[qy+q(1-q)]\). Optimizing over \(q\in[0,1]\) and subtracting the better-anchor value gives \(\varepsilon(1-|y|)^2/4\) on \(|y|<1\), and zero otherwise. The density of \(\Delta\) at zero is asymptotic to
\(b e^{-c/4}/(2\sqrt{\pi c})\); multiply by \(d\Delta=\varepsilon\,dy\) and use
\(\int_{-1}^1(1-|y|)^2/4\,dy=1/6\).
The expansion is uniform for \(c\) in compact positive intervals, since the exact stopping region bounds \(y\) there. Hence the same coefficient, evaluated at \(c_\infty\), applies when full and exterior-only policies optimize their brackets separately, by sandwiching the difference of their maxima between their respective interior premiums.
