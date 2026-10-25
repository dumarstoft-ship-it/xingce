# T239 棱长 7 的涂色立方体：一面涂黑的比两面+三面涂黑的多多少（逐块枚举）
n = 7
c = {0: 0, 1: 0, 2: 0, 3: 0}
for x in range(n):
    for y in range(n):
        for z in range(n):
            k = sum(1 for t in (x, y, z) if t == 0 or t == n - 1)
            c[k] += 1
diff = c[1] - (c[2] + c[3])
options = {"A": 52, "B": 62, "C": 72, "D": 82}
hits = [k for k, v in options.items() if v == diff]
assert len(hits) == 1, (diff, hits)
print(hits[0])
