import json, re, sys
for f in sys.argv[1:]:
    d = json.load(open(f))
    for x in d:
        j = x['jiexi']
        han = len(re.findall(r'[一-鿿]', j))
        nolatex = len(re.sub(r'\$[^$]*\$', 'X', j))
        print(x['vid'], 'raw', len(j), 'han', han, 'nolatex', nolatex)
