"""D05-math-1-v03 验算：广州→香港出行方案。高铁 3 条、城际 2 条到深圳，再经甲/乙口岸；
城际不能衔接甲口岸；另有 2 个直达跨境巴士班次。逐条列出所有方案计数。"""
OPTIONS = {"A": 7, "B": 8, "C": 10, "D": 12}

leg1 = [("高铁", i) for i in range(3)] + [("城际", i) for i in range(2)]
ports = ["甲", "乙"]
plans = []
for line in leg1:
    for port in ports:
        if line[0] == "城际" and port == "甲":
            continue
        plans.append((line, port))
plans += [("直达巴士", i) for i in range(2)]
cnt = len(set(plans))

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
