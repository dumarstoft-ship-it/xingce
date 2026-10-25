"""D05-math-1-v07 验算：3 位取件码，每位从 1-5 和 X、Y、Z 共 8 个字符中选（可重复），
要求既有数字又有字母。穷举全部 8^3 个码。"""
from itertools import product

OPTIONS = {"A": 360, "B": 387, "C": 485, "D": 512}
chars = "12345XYZ"
cnt = sum(1 for code in product(chars, repeat=3)
          if any(c.isdigit() for c in code) and any(c.isalpha() for c in code))

hits = [k for k, v in OPTIONS.items() if v == cnt]
assert len(hits) == 1, (cnt, hits)
print("count =", cnt)
print(hits[0])
