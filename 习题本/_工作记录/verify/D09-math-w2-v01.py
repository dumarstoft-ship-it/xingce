# D09-math-w2-v01: a seed cabinet holds sample bags of 5 rice varieties
# (30, 16, 9, 6, 2 bags); the bags look alike, so the variety of a drawn bag cannot be chosen.
# Fewest bags to draw that GUARANTEES at least 2 varieties with >= 5 bags each.
# Solve by brute force over every possible draw (a_1..a_5 with 0 <= a_i <= n_i):
# the answer is (largest draw that still fails) + 1, then check the guarantee directly.
from itertools import product

n = [30, 16, 9, 6, 2]        # bags per variety (jia, yi, bing, ding, wu)
K = 5                        # each qualifying variety needs at least K bags
NEED = 2                     # at least NEED varieties must qualify


def ok(draw):
    return sum(1 for v in draw if v >= K) >= NEED


draws = list(product(*(range(x + 1) for x in n)))
worst = max(sum(d) for d in draws if not ok(d))
ans = worst + 1
assert ans <= sum(n)
# guarantee check: every draw of size ans works, and some draw of size ans - 1 fails
assert all(ok(d) for d in draws if sum(d) == ans)
assert any(not ok(d) for d in draws if sum(d) == ans - 1)

# the error paths behind the distractors (for information only)
template_plus2 = sum(min(x, K - 1) for x in n) + 2          # "each K-1, then +2"
small_as_full = max(n) + (K - 1) * (len(n) - 1) + 1          # small variety counted as K-1
no_plus_one = worst                                          # forgot the final +1
print('worst failing draw', worst, '-> answer', ans)
print('distractor paths: template+2 =', template_plus2,
      '| small variety as K-1 =', small_as_full, '| no +1 =', no_plus_one)

opts = {'A': 20, 'B': 44, 'C': 45, 'D': 47}
hit = [k for k, v in opts.items() if v == ans]
assert len(hit) == 1, (ans, hit)
print(hit[0])
