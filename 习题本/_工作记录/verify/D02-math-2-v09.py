# D02-math-2-v09：小张单独9小时、小李单独12小时，两人轮流每次1小时。
# 小张先开始比小李先开始提前多少分钟完成。解法：两种顺序分别逐小时模拟（精确分数）。
from fractions import Fraction as F

OPTIONS = {'A': 0, 'B': 5, 'C': 15, 'D': 20}
rate = {'张': F(1, 9), '李': F(1, 12)}


def finish(order):
    done, t, i = F(0), F(0), 0
    while True:
        who = order[i % 2]
        if done + rate[who] >= 1:
            return t + (1 - done) / rate[who]
        done += rate[who]
        t += 1
        i += 1


t_zhang = finish(['张', '李'])
t_li = finish(['李', '张'])
diff = (t_li - t_zhang) * 60
hits = [k for k, v in OPTIONS.items() if v == diff]
assert len(hits) == 1, (diff, hits)
# 干扰项：两种顺序的"尾巴"时长分别为15、20分钟
assert (t_zhang - int(t_zhang)) * 60 == OPTIONS['C'] and (t_li - int(t_li)) * 60 == OPTIONS['D']
print('小张先', t_zhang, '小时；小李先', t_li, '小时；相差', diff, '分钟')
print(hits[0])
