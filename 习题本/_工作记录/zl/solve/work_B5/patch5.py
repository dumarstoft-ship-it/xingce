p = "build_out.py"
s = open(p, encoding="utf-8").read()
def rep(old_start, new_text):
    global s
    i = s.find('r"' + old_start)
    assert i >= 0, old_start
    j = s.find('", ""', i)
    assert j > i
    s = s[:i] + 'r"' + new_text + s[j:]
def sub(old, new):
    global s
    assert s.count(old) == 1, old
    s = s.replace(old, new)
rep("本题考查两期比重比较。利润总额增速", r"本题考查两期比重比较。利润总额增速30.7%高于营业收入增速10.3%，利润率上升，排除A、B。变化量 = 现期比重 × $\frac{a-b}{1+a}$（a、b分别为利润、收入增速）= $\frac{1729.68}{18994.25}\times\frac{30.7\%-10.3\%}{1+30.7\%}\approx 9.1\%\times 0.156\approx 1.4$（个百分点），即由约7.7%升至约9.1%。故正确答案为D。")
sub("与资产：3月50234 < 50392.7；4月50459 < 50472.4；5月50317 < 50496.1；6月51014 > 50906.0。",
    "与资产：3月：50234 < 50392.7；4月：50459 < 50472.4；5月：50317 < 50496.1；6月：51014 > 50906.0。")
sub(r"速算：$\frac{3.19}{9.435}\times 67\%\approx 22.6\%$", r"速算：$\frac{3.19}{9.435}\times 67\%\approx 22.7\%$")
open(p, "w", encoding="utf-8").write(s)
print("patched")
