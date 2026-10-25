# search parameter sets for the 盈盈型 + 新增对象 variant
seed_nums = {5, 4, 8, 12}
res = []
for a in range(3, 12):
    for b in range(a + 1, 14):
        for n in range(15, 41):
            for r1 in range(10, 100):
                r2 = r1 - (b - a) * n
                if r2 < 1:
                    continue
                T = a * n + r1
                for c in range(2, a):
                    if T % c:
                        continue
                    m = T // c
                    new = m - n
                    # wrong formula (sum of leftovers)
                    if (r1 + r2) % (b - a):
                        continue
                    n2 = (r1 + r2) // (b - a)
                    T2 = a * n2 + r1
                    if T2 % c:
                        continue
                    new2 = T2 // c - n2
                    lo = r1 // c if r1 % c == 0 else None
                    if any(x in seed_nums for x in (a, b, c)):
                        continue
                    opts = {new, new2, n, m}
                    if len(opts) < 4:
                        continue
                    if not (5 <= new <= 40):
                        continue
                    if r1 % 10 or r2 % 2:
                        continue
                    res.append((a, r1, b, r2, c, n, T, m, new, new2, lo))
for r in res[:80]:
    print(r)
print(len(res))
