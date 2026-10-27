p = "build_out.py"
s = open(p, encoding="utf-8").read()
old = "平均每吨金额增长率 = $\\frac{-5.15\\%+1.14\\%}"
new = "平均数增长率 = $\\frac{-5.15\\%+1.14\\%}"
assert s.count(old) == 1
s = s.replace(old, new)
old2 = "本题考查平均数增长率（间隔）。2022年重量增速"
new2 = "本题考查平均数增长率（间隔）。平均每吨回收金额 = 金额 ÷ 重量。2022年重量增速"
assert s.count(old2) == 1
s = s.replace(old2, new2)
old3 = "注意“降幅收窄”说明上年降幅更大。故正确答案为C。"
new3 = "“降幅收窄”说明上年降幅更大。故正确答案为C。"
assert s.count(old3) == 1
s = s.replace(old3, new3)
open(p, "w", encoding="utf-8").write(s)
print("patched")
