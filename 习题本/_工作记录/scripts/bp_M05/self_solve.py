"""M05 自解真题验算：从题面数据独立求解，并确认四个选项里恰好一个成立。"""
from fractions import Fraction as F

def pick(options, value):
    hits = [k for k, v in options.items() if v == value]
    assert len(hits) == 1, (options, value, hits)
    return hits[0]

# ---------- 2026GK-68 ----------
# 2023 海外亏损 m，2024 海外利润 2m；国内每年利润 D 不变；2024 总利润 = 1.2 × 2023 总利润。
# 取 m = 1（结果以 m 为单位），枚举/解一次方程：D + 2 = 1.2 (D - 1)
m = F(1)
D = None
for cand in [F(k, 10) for k in range(0, 1000)]:      # 0 ~ 99.9 m 内穷举，步长 0.1m
    if cand + 2 * m == F(6, 5) * (cand - m):
        assert D is None
        D = cand
opts = {'A': 13 * m, 'B': 14 * m, 'C': 15 * m, 'D': 16 * m}
ans1 = pick(opts, D)
print('2026GK-68  国内利润 =', D, 'm  ->', ans1)

# ---------- 2026ZJA-58 ----------
# 盒饭售价 40，奶茶售价 10。套餐1：2盒饭+1奶茶 打九折 获利20；套餐2：4盒饭+3奶茶 打八折 获利24。
# 设盒饭成本 a、奶茶成本 b：2a+b = (2*40+10)*0.9-20 ; 4a+3b = (4*40+3*10)*0.8-24
c1 = F(2 * 40 + 10) * F(9, 10) - 20
c2 = F(4 * 40 + 3 * 10) * F(8, 10) - 24
# 解二元一次方程组（克拉默法则）
det = 2 * 3 - 1 * 4
a = (c1 * 3 - 1 * c2) / det
b = (2 * c2 - 4 * c1) / det
assert 2 * a + b == c1 and 4 * a + 3 * b == c2
diff = (40 - a) - (10 - b)
opts = {'A': F(7), 'B': F(15, 2), 'C': F(8), 'D': F(17, 2)}
ans2 = pick(opts, diff)
print('2026ZJA-58 盒饭成本 =', a, '奶茶成本 =', b, '单件利润差 =', diff, '->', ans2)
