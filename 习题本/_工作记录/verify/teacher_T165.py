# teacher T165（2018北京）整点响铃，每9分钟亮灯，正午同时发生，下一次同时发生是下午几点
OPTS = {'A': 1, 'B': 2, 'C': 3, 'D': 4}
BELL, LIGHT = 60, 9
t = next(t for t in range(1, 24 * 60) if t % BELL == 0 and t % LIGHT == 0)
print('正午后', t, '分钟')
hits = [k for k, v in OPTS.items() if v * 60 == t]
assert len(hits) == 1, hits
print(hits[0])
