from itertools import product
def worst(n, K, NEED):
    best=None
    for a in product(*(range(x+1) for x in n)):
        if sum(1 for v in a if v>=K) < NEED:
            s=sum(a)
            if best is None or s>best[0]: best=(s,a)
    return best
for n,K in [((30,16,9,6,2),5),((28,16,9,7,2),5),((27,14,8,5,1),4)]:
    w=worst(n,K,2)
    print(n,K,'worst',w,'ans',w[0]+1,
          'tmpl+1',sum(min(x,K-1) for x in n)+1,'tmpl+2',sum(min(x,K-1) for x in n)+2,
          'small_as_k1',max(n)+(K-1)*(len(n)-1)+1,
          'second_full',sorted(n)[-2]+sum(min(x,K-1) for x in n)-min(sorted(n)[-2],K-1)+1)
