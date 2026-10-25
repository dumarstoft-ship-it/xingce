# D01-math-2-v02 前30件、后30件好评率（区间重叠），求全天好评率
from fractions import Fraction as Fr

opts = {'A': '54%', 'B': '72%', 'C': '75%', 'D': '90%'}
N = 50
first_n, first_rate = 30, Fr(70, 100)   # 前30件好评率70%
last_n, last_rate = 30, Fr(80, 100)     # 后30件好评率80%
mid_lo, mid_hi, mid_good = 21, 30, 9    # 第21~30件中有9件好评

good_first = first_n * first_rate
good_last = last_n * last_rate
assert good_first.denominator == 1 and good_last.denominator == 1
overlap = range(N - last_n + 1, first_n + 1)        # 两段的重叠部分
assert (overlap.start, overlap.stop - 1) == (mid_lo, mid_hi)

# 分成三段 1~20、21~30、31~50，穷举各段好评数
seg_a = mid_lo - 1
seg_b = mid_hi - mid_lo + 1
seg_c = N - mid_hi
rates = set()
for ga in range(seg_a + 1):
    for gb in range(seg_b + 1):
        for gc in range(seg_c + 1):
            if ga + gb == good_first and gb + gc == good_last and gb == mid_good:
                rates.add(Fr(ga + gb + gc, N))
assert len(rates) == 1, rates
rate = rates.pop()

def pct(s):
    return Fr(int(s.rstrip('%')), 100)

# 干扰项的错误路径
assert (first_rate + last_rate) / 2 == pct(opts['C'])                     # 两个率直接平均
assert Fr(good_first + good_last, N) == pct(opts['D'])                    # 没扣重叠
assert Fr(good_first + good_last - 2 * mid_good, N) == pct(opts['A'])     # 重叠扣两次

hits = [k for k, v in opts.items() if pct(v) == rate]
assert len(hits) == 1, hits
print('rate =', rate)
print(hits[0])
