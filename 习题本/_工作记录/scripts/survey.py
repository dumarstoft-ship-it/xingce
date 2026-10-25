import re, os, sys, glob
D = sys.argv[1]
SECS = ['政治理论','常识判断','言语理解','数量关系','判断推理','科学推理','资料分析']
head_re = re.compile(r'^\s*(?:第[一二三四五六七八]部分|[一二三四五六七八]\s*[\.、．])\s*(政治理论|常识判断|言语理解|数量关系|判断推理|科学推理|资料分析)')
qre = re.compile(r'^\s*(\d{1,3})\s*[\.、．]')
for f in sorted(glob.glob(os.path.join(D,'*.txt'))):
    name = os.path.basename(f)
    if '解析' in name or '答案' in name: continue
    lines = open(f, encoding='utf-8', errors='ignore').read().split('\n')
    heads = []
    for i,l in enumerate(lines):
        m = head_re.match(l)
        if m: heads.append((i, m.group(1)))
    # question numbers per section
    res = []
    for k,(i,s) in enumerate(heads):
        j = heads[k+1][0] if k+1 < len(heads) else len(lines)
        nums = []
        for l in lines[i:j]:
            m = qre.match(l)
            if m:
                n = int(m.group(1))
                if not nums or (n > nums[-1] and n - nums[-1] < 6):
                    nums.append(n)
        if nums: res.append(f"{s}:{nums[0]}-{nums[-1]}({len(nums)})")
        else: res.append(f"{s}:?")
    print(name[:40].ljust(40), ' | '.join(res))
