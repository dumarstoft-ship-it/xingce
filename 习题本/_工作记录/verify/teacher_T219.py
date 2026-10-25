# T219（2010浙江）自然数x除以3余2、除以4余3，x除以12余几。
OPTS = {'A': 1, 'B': 5, 'C': 9, 'D': 11}
rems = {x % 12 for x in range(0, 10 ** 4) if x % 3 == 2 and x % 4 == 3}
assert len(rems) == 1, rems
ans = rems.pop()
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('remainder mod 12 =', ans)
print(hits[0])
