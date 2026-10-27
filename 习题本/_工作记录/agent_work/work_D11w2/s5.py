import random
out=[]
for N in range(100,161):
  for A in range(N//2+5, N-10):
    for B in range(N//2+5, A):
      for k in range(8,21):
        lo = A+B-N
        hi = lo+k
        if hi >= B-8: continue
        corr = A+B-2*hi
        d_min = A-B
        d_ind = N-B-k
        d_max = A+B-2*lo
        d_nk = N-k
        opts = {'corr':corr,'min':d_min,'ind':d_ind,'max':d_max,'N-k':d_nk}
        if len(set(opts.values()))<5: continue
        if min(opts.values())<=0: continue
        out.append((N,A,B,k,opts))
print(len(out))
random.seed(11)
def isAP(v):
    v=sorted(v); d=[v[i+1]-v[i] for i in range(len(v)-1)]; return len(set(d))==1
good=[]
for N,A,B,k,o in out:
    for trio in [('ind','max','min'),('ind','max','N-k'),('ind','min','N-k')]:
        v=[o['corr']]+[o[t] for t in trio]
        if isAP(v): continue
        if any(abs(x-y)<4 for i,x in enumerate(v) for y in v[i+1:]): continue
        good.append((N,A,B,k,o,trio))
print(len(good))
for g in random.sample(good,40): print(g)
