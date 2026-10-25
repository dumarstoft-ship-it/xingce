# D01-math-1-v01  干部网络学院：全年需完成60学时；每月1场直播课（每场2学时）、2次在线测试（每次0.5学时），
# 其余靠观看专题视频（每45分钟折合1学时）。求平均每月需观看专题视频多少小时。
from fractions import Fraction as F

YEAR_REQ, MONTHS = 60, 12
VIDEO_MIN_PER_XS = 45            # 45分钟折合1学时
LIVE_N, LIVE_XS = 1, 2           # 每月直播课场数、每场学时
TEST_N, TEST_XS = 2, F(1, 2)     # 每月测试次数、每次学时
OPTS = {'A': F(3, 2), 'B': F(2), 'C': F(9, 4), 'D': F(18)}

# 穷举每月观看视频的分钟数（1分钟步长），找出使全年学时恰好达到要求的时长
sols = [m for m in range(0, 31 * 24 * 60)
        if (LIVE_N * LIVE_XS + TEST_N * TEST_XS + F(m, VIDEO_MIN_PER_XS)) * MONTHS == YEAR_REQ]
assert len(sols) == 1, sols
hours = F(sols[0], 60)
hits = [k for k, v in OPTS.items() if v == hours]
assert len(hits) == 1, (hours, hits)

# 干扰项来源核对
month_xs = F(YEAR_REQ, MONTHS)
video_xs = month_xs - LIVE_N * LIVE_XS - TEST_N * TEST_XS
assert video_xs == OPTS['B']                                          # 把“学时”直接当“小时”
assert (month_xs - LIVE_N * LIVE_XS) * VIDEO_MIN_PER_XS / 60 == OPTS['C']  # 漏扣在线测试
assert hours * MONTHS == OPTS['D']                                    # 求成全年
print('video minutes per month', sols[0], 'hours', hours)
print(hits[0])
