import json
d = json.load(open('harden/D01_decision.json'))
for x in d['remove']:
    if x['key'] in ('D01-math-1-v07', 'D01-math-2-v01', '2023GD-31', '2024SD-53', 'D01-math-2-v08', 'D01-math-2-v10', 'D01-math-2-v05'):
        print(x['key'], '|', x['why'])
