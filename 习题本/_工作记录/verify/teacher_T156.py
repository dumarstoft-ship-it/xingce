# teacher T156（2022青海）2021年7月1日星期四，2031年7月1日星期几
import datetime as dt

OPTS = {'A': '一', 'B': '二', 'C': '三', 'D': '四'}
WD = ['一', '二', '三', '四', '五', '六', '日']
BASE, BASE_WD = dt.date(2021, 7, 1), '四'
TARGET = dt.date(2031, 7, 1)
delta = (TARGET - BASE).days                     # 只用日历算天数，星期从题给“星期四”推
ans = WD[(WD.index(BASE_WD) + delta) % 7]
print('相隔', delta, '天，余', delta % 7, '->', ans)
hits = [k for k, v in OPTS.items() if v == ans]
assert len(hits) == 1, hits
print(hits[0])
