from fractions import Fraction as F
out = []
for n1 in range(5, 31):
    for h1 in range(4, 31):
        for n2 in range(n1 + 1, 41):
            for h2 in range(2, h1):
                if (h1 * 2 != h2 * 4) and (h1 * 2 != h2 * 3 * 1) and h1 != 2 * h2 and 2 * h1 != 3 * h2: continue
                x = F(n1 * h1 - n2 * h2, h1 - h2)
                if x.denominator != 1 or x < 3: continue
                S = (n1 - x) * h1
                x = int(x); S = int(S)
                if S > 300: continue
                for a in range(2, 11):
                    for b in range(2, 13):
                        for k in range(2, 9):
                            if k == x: continue
                            Nf = F(S + x * (a + b) + k * b, a + b)
                            if Nf.denominator != 1: continue
                            N = int(Nf)
                            if not (12 <= N <= 40) or N - k <= x: continue
                            if N in (n1, n2): continue
                            e1 = F(S + k * b, a + b); e2 = F(S + (k + x) * b, a + b); e5 = N - k
                            e4 = F(S + x * a + k * b, a + b)
                            if any(v.denominator != 1 for v in (e1, e2)): continue
                            opts = sorted({N, int(e1), int(e2), e5})
                            if len(opts) < 4: continue
                            if any(v in (n1, n2) for v in opts): continue
                            gaps = [opts[i + 1] - opts[i] for i in range(3)]
                            if min(gaps) < 2: continue
                            out.append((n1, h1, n2, h2, x, S, N, a, k, b, int(e1), int(e2), e5, e4))
print(len(out))
out.sort(key=lambda r: (r[5], r[7] + r[9]))
for r in out[:80]:
    n1, h1, n2, h2, x, S, N, a, k, b, e1, e2, e5, e4 = r
    print(f"{n1}台{h1}h, {n2}台{h2}h -> x={x} S={S}; N={N} a={a} k={k} b={b}; e1={e1} e2={e2} e5={e5} e4={e4}")
