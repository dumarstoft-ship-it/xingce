# Probe the V1 skeleton: a=2c, a+b=S1, c+d=S3, a>b>c>d>=1
def run(S1, S3, mult=2):
    full, loose = [], []
    for c in range(1, 200):
        a = mult * c; b = S1 - a; d = S3 - c
        if min(a, b, c, d) < 1: continue
        if a > b > c:
            loose.append((a, b, c, d))
            if c > d: full.append((a, b, c, d))
    return full, loose
for S1, S3 in [(60, 37), (72, 45), (84, 51), (66, 41)]:
    f, l = run(S1, S3)
    print(S1, S3, 'full:', f, '| only first two orderings:', [x[2] for x in l])
