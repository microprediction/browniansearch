"""Verify small-positive-b opening asymptotics for grass-compact.pdf.

Requires numpy and scipy. Default prints analytic asymptotic coefficients.
Run python grass_opening_verify.py --numerical for the direct opening checks.
The direct quadrature is intended for 0 < b <= 0.1 and rho near 0.54*b;
it truncates the reveal integral at +/-10 (negligible at displayed precision).
Its derivative uses the bridge envelope and the normal density score,
not finite differences of almost equal objective values.
"""
import math
import numpy as np
from scipy.optimize import brentq
from scipy.integrate import quad

PI0=1/math.sqrt(2*math.pi)

def zeta(x):
    return .5 if x<=0 else ((1+x*x)/2 if x<1 else x)

def bridge(b,d,r):
    B,D=max(b,d),min(b,d)
    # q is correlation to larger anchor
    den=1-r*r
    def der(q):return (B-r*D)-(D-r*B)*r/q**2-q+r*r/q**3
    if der(1)>=0: return (B,0.,1. if d>=b else 0.)
    lo=math.sqrt(r)
    if B==D:
        C=(1+r)/(1-r)
        m=max(2*lo/(1+r), min(1., B/C))
        z=(1+r)*m
        q=.5*(z+math.sqrt(max(0.,z*z-4*r)))
    else:q=brentq(der,lo,1,xtol=1e-15,rtol=1e-14)
    N=(B-r*D)*q+(D-r*B)*r/q+.5*(1+r*r-q*q-r*r/q**2)
    V=N/den
    Nr=-D*q+(D-2*r*B)/q+r-r/q**2
    Vr=(Nr+2*r*V)/den
    Vd=(q-r*r/q)/den if d>=b else r*(1/q-q)/den
    return V,Vr,Vd

def v_all(b,d,r):
    v0=zeta(b);v1=zeta(d)
    if v0>=v1:V,Vr,Vd=v0,0.,0.
    else:V,Vr,Vd=v1,0.,max(0.,min(d,1.))
    vi,vri,vdi=bridge(b,d,r)
    if vi>V:V,Vr,Vd=vi,vri,vdi
    return V,Vr,Vd

def breaks(b,r):
    # resolve all branch crossings adaptively on d∈(0,1)
    def gap(d):return bridge(b,d,r)[0]-max(zeta(b),zeta(d))
    ds=np.unique(np.r_[np.linspace(-1,2,121),b,np.geomspace(1e-10,.01,31)])
    roots=[]
    for d1,d2 in zip(ds[:-1],ds[1:]):
        g1,g2=gap(d1),gap(d2)
        if g1*g2<0:roots.append(brentq(gap,d1,d2,xtol=5e-15))
    return sorted(set([-10.,0.,b,1.,max(1.,(1-r*r+2*r*b)/(1+r*r)),10.]+roots))

def J(b,r):
    s=math.sqrt(1-r*r)
    bs=breaks(b,r)
    def fun(d):
        V,Vr,Vd=v_all(b,d,r)
        z=(d-b*r)/s
        return math.exp(V-.5*z*z)*PI0/s
    def dfun(d):
        V,Vr,Vd=v_all(b,d,r)
        z=(d-b*r)/s
        return math.exp(V-.5*z*z)*PI0/s*(Vr+b*z/s+r*(1-z*z)/(s*s))/b
    val=sum(quad(fun,x,y,epsabs=2e-12,epsrel=2e-12,limit=200)[0] for x,y in zip(bs[:-1],bs[1:]))
    grad=sum(quad(dfun,x,y,epsabs=2e-11,epsrel=2e-11,limit=200)[0] for x,y in zip(bs[:-1],bs[1:]))
    return val,grad,bs


def asymptotic_coefficients():
    p=PI0
    def equation(a):
        return ((1+a*a)*math.log(a)+2-a*a/2+a**4/6
                -math.sqrt(math.pi/2)*(1-a)**2)
    a=brentq(equation,.01,.9,xtol=1e-15)
    k=2*a/(1+a*a)
    ap=(1+a*a)**2/(2*(1-a*a))
    B=.25+2*p/3
    def terms(d):
        A=1/d-d
        C=(1/d**2-d*d)/2
        f=k*A-k*k*C
        fk=A-2*k*C
        q=-k*(1+1/d**2)+k*k*(1/d+1/d**3)
        qk=-(1+1/d**2)+2*k*(1/d+1/d**3)
        u=k*d+.5*k*k*(1-d*d)
        uk=d+k*(1-d*d)
        H=k*k*f+.5*q*q+.5*f*f+f*u
        Hk=2*k*f+k*k*fk+q*qk+f*fk+fk*u+f*uk
        return f,H,Hk
    Q=.25+(1+p)*k/2-B*k*k+p*quad(lambda d:terms(d)[0],a,1)[0]
    Qpp=-.5+p*(-1/(2*a)+a+a**3/6)
    S=(1/16-p*k/2+B*k*k-(.25+7*p/8)*k**3
       +(1/16+3*p/20)*k**4+p*quad(lambda d:terms(d)[1],a,1)[0])
    Sp=(-p/2+2*B*k-3*(.25+7*p/8)*k*k
        +4*(1/16+3*p/20)*k**3
        +p*(quad(lambda d:terms(d)[2],a,1,epsabs=1e-13)[0]
            -ap*terms(a)[1]))
    eta=-Sp/Qpp
    theta=-p*k/(3*Qpp)
    print(f'a = {a:.15f}')
    print(f'kappa = {k:.15f}')
    print(f'1/sqrt(pi) = {1/math.sqrt(math.pi):.15f}')
    print(f'cubic coefficient = {eta:.15f}')
    print(f'quartic coefficient = {theta:.15f}')
    print(f'exterior-only kappa = {(1+p)/(1+8*p/3):.15f}')
    print(f'Q = {Q:.15f}, Q second derivative = {Qpp:.15f}')
    print(f'S = {S:.15f}, S derivative = {Sp:.15f}')
    print(f'log-value b2 coefficient = {Q/(1+p):.15f}')
    return k

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--numerical',action='store_true')
    parser.add_argument('--b',type=float,nargs='+',default=[.1,.03,.01,.003,.001,.0003])
    args=parser.parse_args()
    kappa=asymptotic_coefficients()
    if args.numerical:
        print('b                  rho/b              log expected payoff')
        for b in args.b:
            if not 0 < b <= .1:
                raise ValueError('Direct check is scoped to 0 < b <= 0.1.')
            k=brentq(lambda k:J(b,k*b)[1],.48,.58,xtol=1e-12)
            val,grad,bs=J(b,k*b)
            print(f'{b:<18.8g} {k:<18.12f} {math.log(val):.12f}',flush=True)
