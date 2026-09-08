"""Verify the Lambert-W opening coefficient in Euclidean dimension >=2.

Requires numpy and scipy. All correlation geometry and terminal optimizers are
included; no imports from another project file. Direct integration is scoped
to small positive b and rho near 0.604*b, truncating the normal reveal at +/-10.
Usage: python grass_spatial_verify.py --b .01 .001 .0003
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


p=PI0

def vplane(b,d,r):
    V,Vr,Vd=v_all(b,d,r)
    if d>=r*b and b>=r*d and b*d<=r:
        den=1-r*r
        Vf=.5+.5*(b*b-2*r*b*d+d*d)/den
        if Vf>V:
            V=Vf
            Vr=(r*(b*b+d*d)-b*d*(1+r*r))/den**2
            Vd=(d-r*b)/den
    return V,Vr,Vd

def J(b,r):
    s=math.sqrt(1-r*r)
    bs=sorted(set([-10.,0.,b,1.,r*b,r/b,b/r,max(1.,(1-r*r+2*r*b)/(1+r*r)),10.]))
    def fun(d):
        V,Vr,Vd=vplane(b,d,r);z=(d-b*r)/s
        return math.exp(V-.5*z*z)*p/s
    def dfun(d):
        V,Vr,Vd=vplane(b,d,r);z=(d-b*r)/s
        return math.exp(V-.5*z*z)*p/s*(Vr+b*z/s+r*(1-z*z)/(s*s))/b
    val=sum(quad(fun,x,y,epsabs=2e-12,epsrel=2e-12,limit=200)[0] for x,y in zip(bs[:-1],bs[1:]))
    grad=sum(quad(dfun,x,y,epsabs=2e-11,epsrel=2e-11,limit=200)[0] for x,y in zip(bs[:-1],bs[1:]))
    return val,grad


if __name__=='__main__':
    import argparse
    from scipy.special import lambertw
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--b',nargs='+',type=float,default=[.1,.01,.001,.0003])
    args=parser.parse_args()
    c=math.sqrt(math.pi/2)
    kappa=float(lambertw(c*math.exp(c-1)).real)/c
    print(f'Lambert-W coefficient: {kappa:.15f}')
    print('b                  optimal rho/b         inferred cubic coefficient')
    for b in args.b:
        if not 0 < b <= .1:
            raise ValueError('This direct check is scoped to 0 < b <= 0.1.')
        k=brentq(lambda k:J(b,k*b)[1],.55,.66,xtol=1e-12)
        val,_=J(b,k*b)
        print(f'{b:<18.8g} {k:<21.12f} {(k-kappa)/b**2:.10f}',flush=True)
