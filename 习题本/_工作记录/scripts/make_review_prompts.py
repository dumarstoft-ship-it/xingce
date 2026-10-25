"""Create blind-review files + prompt for a (day, part) after generation is complete."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from prompts import review_prompt, S
from strip_answers import strip
def make(day, part):
    sched = json.load(open(S + '/db/schedule.json'))['schedule'][day - 1]
    module = sched[part]
    os.makedirs(S + '/review', exist_ok=True)
    q = f'{S}/review/D{day:02d}_{part}_questions.json'
    k = f'{S}/review/D{day:02d}_{part}_key.json'
    n = strip(f'D{day:02d}_{part}_*.json', q, k)
    out = f'{S}/review/D{day:02d}_{part}_review.json'
    pf = f'{S}/prompts/rev_D{day:02d}_{part}.txt'
    open(pf, 'w').write(review_prompt(day, part, module, q, k, out))
    return {'prompt': pf, 'n': n, 'out': out}
if __name__ == '__main__':
    for arg in sys.argv[1:]:
        d, p = arg.split(':')
        print(arg, make(int(d), p))
