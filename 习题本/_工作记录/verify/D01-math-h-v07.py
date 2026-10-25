# D01-math-h-v07  预制菜加工坊三人合伙（修订版：反求撤资月份）：
# 甲年初出资30万元，全年不变；乙年初出资80万元，年内某月初撤回其中40万元；丙8月初加入，出资80万元；
# 除此之外出资均无变动。年终利润全部按“出资额×出资月数”的比例分配，乙分得的利润恰好是丙的2倍。
# 求乙在几月初撤回40万元。
from fractions import Fraction as F

OPTS = {'A': 5, 'B': 7, 'C': 8, 'D': 9}
JIA, YI0, YI_OUT, BING, BING_JOIN, RATIO = 30, 80, 40, 80, 8, 2


def capital(person, month, w):
    """month = 1..12；w = 乙撤资的月份（w月初撤回）"""
    if person == 'jia':
        return JIA
    if person == 'yi':
        return YI0 if month < w else YI0 - YI_OUT
    if person == 'bing':
        return BING if month >= BING_JOIN else 0
    raise ValueError(person)


def weight(person, w):
    return sum(capital(person, m, w) for m in range(1, 13))


# 穷举撤资月份：w月初撤资，w = 1..12
sols = [w for w in range(1, 13) if weight('yi', w) == RATIO * weight('bing', w)]
assert len(sols) == 1, sols
w = sols[0]
hits = [k for k, v in OPTS.items() if v == w]
assert len(hits) == 1, hits
# 甲的出资不影响乙、丙之比（题中多给的条件）：把甲的出资换成别的值，解不变
for jia_alt in (10, 50, 100):
    JIA = jia_alt
    assert [x for x in range(1, 13) if weight('yi', x) == RATIO * weight('bing', x)] == [w]
JIA = 30

# 干扰项来源核对
need = RATIO * weight('bing', w)
assert w - 1 == OPTS['C']                                                  # 把“80万元出资了8个月”答成8月
assert [x for x in range(1, 13) if YI0 * x + (YI0 - YI_OUT) * (13 - x) == need] == [OPTS['B']]   # 月数两头都算
bing_wrong = BING * (12 - BING_JOIN)                                       # 丙按“12−8＝4”个月算
assert [x for x in range(1, 13)
        if YI0 * (x - 1) + (YI0 - YI_OUT) * (13 - x) == RATIO * bing_wrong] == [OPTS['A']]
print('yi weight', weight('yi', w), 'bing weight', weight('bing', w), 'w =', w)
print(hits[0])
