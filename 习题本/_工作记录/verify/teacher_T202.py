# T202（2013广州）审核1.5分钟/份、通过率1/3，缴费50秒/份，共10人，1号窗口安排几人效率最高。
from fractions import Fraction as F

STAFF, AUDIT, PASS, PAY = 10, F(3, 2), F(1, 3), F(50, 60)
OPTS = {'A': 9, 'B': 8, 'C': 7, 'D': 6}


def throughput(x):
    y = STAFF - x
    return min(x / AUDIT * PASS, y / PAY)   # 每分钟完成缴费的人数，由较慢一环决定


best_x = max(range(1, STAFF), key=throughput)
assert sum(1 for x in range(1, STAFF) if throughput(x) == throughput(best_x)) == 1
hits = [k for k, v in OPTS.items() if v == best_x]
assert len(hits) == 1, (best_x, hits)
print({x: float(throughput(x)) for x in range(1, STAFF)})
print(hits[0])
