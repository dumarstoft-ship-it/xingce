# -*- coding: utf-8 -*-
"""逐条验算改编 idea：python3 run_verify.py [ideas_d03 ideas_d17 ...]"""
import sys, importlib, collections, time
sys.path.insert(0, '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad/bp_M04_work/v2')
import vcommon
mods = sys.argv[1:] or ['ideas_d03', 'ideas_d17', 'ideas_d31', 'ideas_d40', 'ideas_backup']
for m in mods:
    importlib.import_module(m)
ok = 0
letters = collections.Counter()
dirs = collections.Counter()
for v in vcommon.REGISTRY:
    t0 = time.time()
    val = v.verify()
    dt = time.time() - t0
    ok += 1
    letters[(v.day, v.ans)] += 1
    dirs[(v.day, v.direction)] += 1
    print('OK %-8s 考法%-2d %s 答案%s 值=%s  (%.1fs)' % (v.tag(), v.kf, v.direction, v.ans, val, dt))
print('通过', ok, '条')
for d in sorted(set(k[0] for k in letters)):
    print('第%d天 答案分布' % d, {L: letters[(d, L)] for L in 'ABCD'}, ' 方向', {x: dirs[(d, x)] for x in ('巩固', '深化', '拓展')})
