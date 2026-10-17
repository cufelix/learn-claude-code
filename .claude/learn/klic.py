"""Overeny klic + kontrola. Pouziti:
  python3 klic.py            -> selftest: klic vs. sympy.solveset na mnoha hodnotach parametru
  python3 klic.py PRIKLAD p=2 [q=1]   -> vypise spravnou mnozinu reseni pro dane parametry
  python3 klic.py PRIKLAD p=2 x=5     -> overi, zda x resi puvodni rovnici (vcetne DO)
"""
import sys
from sympy import *
x,y,p,q,t,a = symbols('x y p q t a', real=True)
R, E = S.Reals, S.EmptySet
def F(*v): return FiniteSet(*v)
inf = oo
# id: (promenna, lhs, rhs, parametry, klic(par...) -> mnozina)
def r(v): return Rational(v) if not isinstance(v,Basic) else v
EX = {
 'lin1': (x, 2*x*p+p*(1-x), 3*p-4+2*x, [p], lambda p: R if p==2 else F(2)),
 'lin3': (x, t*(3+t)*x, 2*t, [t], lambda t: R if t==0 else E if t==-3 else F(2/(3+t))),
 'lin5': (x, x*(p**2-1), p**2+p, [p], lambda p: E if p==1 else R if p==-1 else F(p/(p-1))),
 'lin6': (x, p*(x*p-1), 1-x, [p], lambda p: F((p+1)/(p**2+1))),
 'lin7': (x, p*(x*p+1), 2*(x+1)+x*p, [p], lambda p: R if p==2 else E if p==-1 else F(-1/(p+1))),
 'pod1': (x, t/(x-2), 2/(x-t), [t], lambda t: R-F(2) if t==2 else E if t==0 else F(t+2)),
 'pod2': (x, 3*x/(x+2), t/(t-1), [t], lambda t: E if t==Rational(3,2) else F(2*t/(2*t-3))),
 'pod4': (x, x*p**2+4*x*q**2, p**2-4*q**2, [p,q], lambda p,q: R if p==q==0 else F((p**2-4*q**2)/(p**2+4*q**2))),
 'pod5': (x, p**2*x-q**2*x, p+q, [p,q], lambda p,q: R if p+q==0 else E if p==q else F(1/(p-q))),
 'kv1': (x, t*x**2+t**2*x+t, 0, [t], lambda t: R if t==0 else E if abs(t)<2 else F(-t/2) if abs(t)==2 else F((-t+sqrt(t**2-4))/2,(-t-sqrt(t**2-4))/2)),
 'kv3': (y, (y**2+3*y)/(3-a), 1, [a], lambda a: E if a>Rational(21,4) else F(Rational(-3,2)) if a==Rational(21,4) else F((-3+sqrt(21-4*a))/2,(-3-sqrt(21-4*a))/2)-(F(0,-3) if a==3 else E)),
 'kv4': (x, x**2-t*x**2+t*x-2*x+1, 0, [t], lambda t: F(1) if t==1 else F(1,1/(1-t))),
 'irr2': (x, sqrt(x**2+3*p**2), x+p, [p], lambda p: Interval(0,inf) if p==0 else F(p) if p>0 else E),
 'irr3': (y, a*sqrt(y+a), a**2, [a], lambda a: Interval(0,inf) if a==0 else F(a**2-a) if a>0 else E),
 'irr4': (x, sqrt(x**2-1), x-p, [p], lambda p: E if p==0 else F((p**2+1)/(2*p)) if (p>0 and p<=1) or p<=-1 else E),
}
# sympy.solveset ignoruje definicni obor po zkraceni / pro a=0 — tady je spravne klic (overeno rucne)
SYMPY_DOMAIN_BUGS = {('pod1', (2,)), ('irr3', (0,))}
DOM = {'kv3': lambda a: a!=3, 'pod2': lambda t: t!=1}  # parametry, kde rovnice neni definovana
def true_set(k, vals):
    v, l, rr, ps, _ = EX[k]; s = dict(zip(ps, vals))
    if k in DOM and not DOM[k](*vals): return None
    return solveset((l-rr).subs(s), v, R)
def selftest():
    G = [Rational(n,d) for n in range(-12,13) for d in (1,2,3)]
    G = sorted(set(G+[Rational(21,4),Rational(3,2)]))
    bad=0; n=0
    for k,(v,l,rr,ps,key) in EX.items():
        grids = [G] if len(ps)==1 else [[-2,-1,0,1,2,3]]*2
        import itertools
        for vals in itertools.product(*grids):
            ts = true_set(k, vals)
            if ts is None: continue
            ks = key(*vals); n+=1
            if (k=='kv3' and vals[0]==3) or (k, tuple(vals)) in SYMPY_DOMAIN_BUGS: continue
            if simplify(Union(ts-ks, ks-ts)) is not E and Union(ts-ks, ks-ts)!=E:
                bad+=1; print('MISMATCH',k,vals,'sympy',ts,'key',ks)
    print(f'{n} kontrol, {bad} nesouladu')
if __name__=='__main__':
    a_=sys.argv[1:]
    if not a_: selftest()
    else:
        if a_[0] not in EX: sys.exit(f"Neznamy priklad {a_[0]!r}. Dostupne: {', '.join(EX)}")
        k=a_[0]
        # jen cisla / zlomky — zadne sympify (eval), skript je v allowlistu bez potvrzeni
        import re
        NUM=re.compile(r'^-?\d+(\.\d+)?(/\d+)?$')
        bad=[s for s in a_[1:] if '=' not in s or not NUM.match(s.split('=',1)[1])]
        if bad: sys.exit(f"Hodnoty musi byt cisla nebo zlomky (napr. p=-3/2): {bad}")
        kv={s.split('=',1)[0]:Rational(s.split('=',1)[1]) for s in a_[1:]}
        v,l,rr,ps,key=EX[k]; vals=[kv[str(s)] for s in ps]
        if str(v) in kv:
            s=dict(zip(ps,vals)); s[v]=kv[str(v)]
            print('RESI' if simplify((l-rr).subs(s))==0 and (l.subs(s).is_real and rr.subs(s).is_real) else 'NERESI')
        else: print(key(*vals))
