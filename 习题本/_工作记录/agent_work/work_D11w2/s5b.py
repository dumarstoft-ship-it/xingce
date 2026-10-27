import random
out=[]
for N in range(120,151):
  for A in range(N//2+10, N-15):
    for B in range(N//2+10, A):
      for k in range(10,21):
        lo = A+B-N
        hi = lo+k
        if hi > B-15: continue
        corr = A+B-2*hi
        o={'corr':corr,'min':A-B,'ind':N-B-k,'max':A+B-2*lo,'N-k':N-k}
        if not (40<=corr<=80 and 5<=o['min']<=20): continue
        vals=list(o.values())
        if len(set(vals))<5: continue
        if set(vals)&{N,A,B,k,lo,hi}: continue
        if N%10==0 or k%5==0: continue
        out.append((N,A,B,k,lo,hi,o))
print(len(out))
random.seed(2)
for g in random.sample(out,30): print(g)
