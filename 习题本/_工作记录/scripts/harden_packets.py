"""Add the teacher's questions (teacher/bank_B*.json, keep=true) of each day's module to the week-1 harden packets."""
import json, glob, re
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'

def main():
    ex = {e['tid']: e for e in json.load(open(S + '/teacher/examples.json'))}
    bank = [b for f in sorted(glob.glob(S + '/teacher/bank_B*.json')) for b in json.load(open(f)) if b.get('keep')]
    for d in range(1, 8):
        p = f'{S}/harden/D0{d}_packet.json'
        pk = json.load(open(p))
        week_ids = {it.get('id') for it in pk['items'] if it['type'] == 'real'}
        items = []
        for b in bank:
            if b.get('module') != pk['module']: continue
            items.append({'tid': b['tid'], 'source': b.get('source'), 'db_match': b.get('db_match'),
                          'already_in_day': b.get('db_match') in week_ids, 'level': b.get('level'), 'method': b.get('method'),
                          'kaofa': b.get('kaofa'), 'learn': b.get('learn'), 'stem': b.get('stem'), 'options': b.get('options'),
                          'answer': b.get('answer'), 'jiexi': b.get('jiexi'), 'has_figure': bool(b.get('figure')),
                          'review_crop': ex[re.sub(r'x\d+$', '', b['tid'])]['review_crop'], 'section': ex[re.sub(r'x\d+$', '', b['tid'])]['section']})
        pk['teacher'] = items
        json.dump(pk, open(p, 'w'), ensure_ascii=False, indent=1)
        print(d, pk['module'], 'teacher items', len(items), 'already in day', sum(i['already_in_day'] for i in items))

if __name__ == '__main__':
    main()
