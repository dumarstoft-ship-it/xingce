import re, json
def vis(s):
    t = re.sub(r'\\(le|ge|times|frac)', 'x', s)
    t = t.replace('$', '').replace('{', '').replace('}', '')
    return len(t)
j1 = ("卡点：约简后用整除定步长，再按两端边界数个数。设大米 x 袋、油 y 桶，$48x+60y=2700$ 约去 12 得 $4x+5y=225$，"
      "225、$5y$ 都是 5 的倍数，故 x 是 5 的倍数。设 $x=5k$，则 $y=45-4k$（米多 5 袋，油少 4 桶）。"
      "$y\\ge1$ 得 $k\\le11$；$x\\ge y$ 得 $k\\ge5$。k 取 5～11，共 7 种，选 B。"
      "易错：漏看“大米不少于食用油”得 11；再算上全换油的 (0, 45) 得 12；把“不少于”当“多于”漏掉 x=y=25，或项数忘了加 1，得 6。")
print(len(j1), vis(j1)); print(j1)
# D07 sample for comparison
v = json.load(open('../gen/D07_math_h.json'))
for x in v: print('D07 sample', len(x['jiexi']), vis(x['jiexi']))
