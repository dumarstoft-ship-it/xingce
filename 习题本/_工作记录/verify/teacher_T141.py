# teacher T141（2013四川下）通知50位同学，每通知一人1分钟，接到通知者也可继续通知，至少几分钟
OPTS = {'A': 5, 'B': 6, 'C': 7, 'D': 8}
STUDENTS = 50
informed, t = 1, 0                # informed 含老师
while informed - 1 < STUDENTS:
    t += 1
    informed *= 2                  # 每个已知者每分钟再通知一个人
print('分钟', t, '| 已通知学生', informed - 1)
hits = [k for k, v in OPTS.items() if v == t]
assert len(hits) == 1, hits
print(hits[0])
