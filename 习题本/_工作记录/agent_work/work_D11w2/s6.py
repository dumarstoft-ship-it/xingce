import itertools, random
out=[]
for P in range(52,81):
  if P in (55,60,65,75,80,70): continue
  for C in range(6,13):
    for A in range(P//2, P):
      for B in range(P//2, A):
        S=A+B+C; D=S-P
        if D<=2*C+4: continue          # min-set cap must bite (well below D/2)
        if A+B-P < C: continue         # construction exists with all of C in triple
        corr=D-C
        o={'corr':corr,'half':D-D//2,'zero':D,'ex2':D-2*C}
        v=list(o.values())
        if len(set(v))<4: continue
        if any(abs(x-y)<4 for i,x in enumerate(v) for y in v[i+1:]): continue
        if set(v)&{P,A,B,C}: continue
        out.append((P,A,B,C,D,o))
print(len(out))
random.seed(4)
for g in random.sample(out,30): print(g)
