# T238 涂色立方体：一面涂黑的个数 = 无涂黑的个数，求棱长（逐块枚举计数）
def counts(n):
    c = {0: 0, 1: 0, 2: 0, 3: 0}
    for x in range(n):
        for y in range(n):
            for z in range(n):
                k = sum(1 for t in (x, y, z) if t == 0 or t == n - 1)
                c[k] += 1
    return c
sol = [n for n in range(3, 25) if counts(n)[1] == counts(n)[0]]
assert len(sol) == 1, sol
options = {"A": 4, "B": 6, "C": 16, "D": 8}
hits = [k for k, v in options.items() if v == sol[0]]
assert len(hits) == 1
print(hits[0])
