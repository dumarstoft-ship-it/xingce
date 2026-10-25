# teacher T138（2020浙江B）答对+10、答错-5、不答-3，三者题数成等差数列，总分95，求总题数
OPTS = {'A': 15, 'B': 30, 'C': 36, 'D': 45}
totals = {}
for right in range(0, 300):
    for wrong in range(0, 300):
        blank = 2 * wrong - right              # 答对、答错、不答依次成等差
        if blank < 0:
            continue
        if 10 * right - 5 * wrong - 3 * blank == 95:
            totals.setdefault(right + wrong + blank, []).append((right, wrong, blank))
hits = [k for k, v in OPTS.items() if v in totals]
print({OPTS[k]: totals[OPTS[k]] for k in hits})
assert len(hits) == 1, hits
print(hits[0])
