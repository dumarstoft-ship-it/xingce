# D04-math-h-v07: a community canteen for the elderly. Monthly fixed spending (rent, wages, ...) is constant
# and so is the food cost per meal; the average cost per meal = monthly fixed spending / meals that month
# + food cost per meal. In March the number of meals was 25% higher than in January and the average cost per
# meal 10% lower. If some month serves twice January's meals, by what percentage is its average cost per
# meal lower than January's?
# Method: January meals Q = 1000; brute force over fixed spending F = 100..200000 and food cost m = 1..60
# (yuan), keep every pair satisfying the March condition exactly, compute the decrease at 2Q for each, and
# check that all admissible pairs give the same decrease. Then match against the options.
from fractions import Fraction as Fr

OPTIONS = {'A': 40, 'B': 50, 'C': 20, 'D': 25}   # rotated ascending order (keeps the 40% linear trap)
Q = Fr(1000)


def avg(fixed, food, meals):
    return fixed / meals + food


decreases = set()
count = 0
for food in range(1, 61):
    for fixed in range(100, 200001, 100):
        a1 = avg(Fr(fixed), Fr(food), Q)
        if avg(Fr(fixed), Fr(food), Q * Fr(125, 100)) == a1 * Fr(90, 100):
            count += 1
            decreases.add((1 - avg(Fr(fixed), Fr(food), 2 * Q) / a1) * 100)
assert count > 0 and len(decreases) == 1, (count, decreases)
dec = decreases.pop()
print(count, 'admissible (fixed, food) pairs; decrease at twice the meals =', dec, '%')
hits = [k for k, v in OPTIONS.items() if Fr(v) == dec]
assert len(hits) == 1, hits

# distractors reproduce the error paths named in the 解析
assert Fr(10) * (2 - 1) / Fr(25, 100) == OPTIONS['A']          # linear: 25% more meals -> 10% lower, so 100% more -> 40%
share_wrong = Fr(10, 100) / Fr(25, 100)                        # fixed part assumed to fall 25% too -> share 40%
assert share_wrong * Fr(1, 2) * 100 == OPTIONS['C']
assert Fr(1, 2) * 100 == OPTIONS['B']                          # everything treated as fixed spending
print(hits[0])
