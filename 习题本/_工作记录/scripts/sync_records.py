"""Copy the scratchpad state needed to resume work into the repo (习题本/_工作记录). Text files only for agent work dirs."""
import os, shutil, glob
S = '/tmp/claude-0/-home-user-xingce/88bc77ab-be1a-5cff-a4a7-35b764f8964e/scratchpad'
D = '/home/user/xingce/习题本/_工作记录'
FULL = ['briefs', 'blueprints', 'cls', 'gen', 'gen_unused', 'prompts', 'review', 'scripts', 'tasks_in', 'verify', 'teacher', 'harden', 'cropfix', 'zl']
DB = ['real_raw.json', 'schedule.json', 'answer_fixes.json', 'overrides.json', 'real_overrides.json', 'recrop.json', 'ocr_answers.json',
      'math_harden.json', 'realonly_plan.json', 'realonly_frozen.json', 'doc_offsets.json',
      'zl_raw.json', 'zl_dups.json', 'zl_fixes.json', 'zl_incomplete.json', 'zl_meta_all.json', 'zl_pool.json', 'zl_rank.json', 'zl_sets.json', 'zl_plan.json']
TEXT_EXT = ('.py', '.md', '.json', '.txt', '.jsonl')
WORK = ['bp_*', 'bpC*', 'work_*', 'rev_*_work', 'l03_build']

def copytree_text(src, dst):
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for f in files:
            if f.endswith(TEXT_EXT) and os.path.getsize(os.path.join(root, f)) < 3_000_000:
                rel = os.path.relpath(os.path.join(root, f), src)
                os.makedirs(os.path.dirname(os.path.join(dst, rel)), exist_ok=True)
                shutil.copy2(os.path.join(root, f), os.path.join(dst, rel))

def main():
    for d in FULL:
        if os.path.exists(f'{S}/{d}'):
            if os.path.exists(f'{D}/{d}'): shutil.rmtree(f'{D}/{d}')
            copytree_text(f'{S}/{d}', f'{D}/{d}')
    os.makedirs(f'{D}/db', exist_ok=True)
    for f in DB:
        if os.path.exists(f'{S}/db/{f}'): shutil.copy2(f'{S}/db/{f}', f'{D}/db/{f}')
    for pat in WORK:
        for p in glob.glob(f'{S}/{pat}'):
            if os.path.isdir(p): copytree_text(p, f'{D}/agent_work/{os.path.basename(p)}')
    for f in ('NOTES_pending.md', 'taxonomy.md'):
        shutil.copy2(f'{S}/{f}', f'{D}/{f}')
    print('synced')

if __name__ == '__main__':
    main()
