# teacher T163（2025行政执法）周一到周四夜跑，2月跑17次、3月跑19次，4月跑几次
OPTS = {'A': 16, 'B': 17, 'C': 18, 'D': 19}
RUN = {0, 1, 2, 3}                                 # 0=周一

def count(start, days):
    return sum((start + d) % 7 in RUN for d in range(days))

res = set()
for leap in (False, True):
    feb = 29 if leap else 28
    for feb1 in range(7):
        mar1 = (feb1 + feb) % 7
        apr1 = (mar1 + 31) % 7
        if count(feb1, feb) == 17 and count(mar1, 31) == 19:
            res.add(count(apr1, 30))
            print('2月', feb, '天, 3月1日周', mar1 + 1, ', 4月1日周', apr1 + 1, ', 4月跑', count(apr1, 30))
assert len(res) == 1
hits = [k for k, v in OPTS.items() if v in res]
assert len(hits) == 1, hits
print(hits[0])
