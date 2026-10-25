# T188（2008浙江）100题，小明对68、小刚对58、小红对78，三人都做对的题至少几题。
# 穷举韦恩图各区域（题目数），找三人都对区域的最小可行值。
Q, A, B, C = 100, 68, 58, 78
OPTS = {'A': 4, 'B': 8, 'C': 12, 'D': 16}


def feasible(t):
    for ab in range(0, min(A, B) - t + 1):
        for ac in range(0, min(A, C) - t - ab + 1):
            a_only = A - t - ab - ac
            if a_only < 0:
                continue
            for bc in range(0, min(B, C) - t + 1):
                b_only = B - t - ab - bc
                c_only = C - t - ac - bc
                if b_only < 0 or c_only < 0:
                    continue
                none = Q - (t + ab + ac + bc + a_only + b_only + c_only)
                if none >= 0:
                    return True
    return False


ans = next(t for t in range(0, min(A, B, C) + 1) if feasible(t))
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, (ans, hits)
print('min all-correct =', ans)
print(hits[0])
