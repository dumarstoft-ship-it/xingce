# D01-math-2-v07 积分两次等价代换（食用油-洗洁精-抽纸）+ 最多（向下取整）
opts = {'A': 27, 'B': 28, 'C': 33, 'D': 45}
# 2桶食用油 = 5瓶洗洁精；2瓶洗洁精 = 3包抽纸
total_oil = 12               # 积分恰好可兑换12桶食用油
used_oil, used_soap = 3, 4   # 先兑换3桶食用油和4瓶洗洁精

answers = set()
cases = 0
for s in range(1, 3001):                  # 每瓶洗洁精所需积分（正整数）
    if (5 * s) % 2 or (2 * s) % 3:
        continue
    r = 5 * s // 2                        # 每桶食用油
    t = 2 * s // 3                        # 每包抽纸
    assert 2 * r == 5 * s and 2 * s == 3 * t
    total = total_oil * r
    remain = total - used_oil * r - used_soap * s
    answers.add(remain // t)
    cases += 1
assert cases > 0 and len(answers) == 1, answers
ans = answers.pop()

# 干扰项的错误路径（取洗洁精6分的一组）
s, r, t = 6, 15, 4
rem = total_oil * r - used_oil * r - used_soap * s
assert round(rem / t) == opts['B']                          # 四舍五入
assert (total_oil * r - used_oil * r) // t == opts['C']   # 漏扣洗洁精
assert (total_oil * r) // t == opts['D']                   # 忘了扣已兑换的

hits = [k for k, v in opts.items() if v == ans]
assert len(hits) == 1, hits
print('max tissue packs =', ans)
print(hits[0])
