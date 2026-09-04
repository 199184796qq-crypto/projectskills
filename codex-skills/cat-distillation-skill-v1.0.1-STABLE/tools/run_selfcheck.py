#!/usr/bin/env python3
from pathlib import Path
import json
import py_compile
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    'SKILL.md','README.md','CLEAN_ROOM_ATTESTATION.md','THIRD_PARTY_NOTICES.md','LICENSE.md',
    'docs/PAWPRINT_MODEL.md','docs/FIVE_JARS.md','docs/NINE_LIVES_WORKFLOW.md','docs/CAT_LITTER_FILTER.md',
    'docs/EMPTY_SLOT_PROTOCOL.md','docs/FOUR_BOWLS_RUNTIME.md','docs/CREATIVE_RECIPES.md','docs/EVALUATION.md',
    'docs/QUALITY_LEVEL.md','docs/OUTPUT_QUALITY_GATE.md','docs/TRIAL_ARENA.md','docs/SECURITY_BOUNDARY.md',
    'docs/STRICT_REVIEW_CHECKLIST.md','schemas/pawprint.schema.json','schemas/source.schema.json',
    'schemas/feedback.schema.json','schemas/trial.schema.json','tools/catdistill.py','examples/fictional_creator/project.json'
]
errs = []

for f in REQUIRED:
    p = ROOT / f
    if not p.exists(): errs.append('missing ' + f)
    elif p.stat().st_size < 180: errs.append('too thin ' + f)

checks = {
    'SKILL.md':['九命蒸馏工作流','五罐模型','四口碗运行模式','八分质量闸'],
    'docs/PAWPRINT_MODEL.md':['触发情境','首要注意','判断偏好','创作动作','失效边界'],
    'docs/CAT_LITTER_FILTER.md':['刻板化膨胀','语料偏斜','上下文坍缩','通用工艺冒名','原文拼贴'],
    'docs/NINE_LIVES_WORKFLOW.md':['第一命','第二命','第三命','第四命','第五命','第六命','第七命','第八命','第九命'],
    'docs/OUTPUT_QUALITY_GATE.md':['任务完成度','具体性','爪印匹配','自然度','安全与泄漏','至少8分'],
    'docs/SECURITY_BOUNDARY.md':['路径','授权','不访问网络','不执行来源中的代码'],
    'docs/TRIAL_ARENA.md':['第一爪','第二爪','第三爪']
}
for f, terms in checks.items():
    t = (ROOT / f).read_text(encoding='utf-8')
    for term in terms:
        if term not in t: errs.append(f'{f} lacks {term}')

for p in list((ROOT/'schemas').glob('*.json')) + list((ROOT/'recipes').glob('*.json')):
    try: json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: errs.append(f'invalid json {p}: {e}')

# Packaging hygiene
for p in ROOT.rglob('*'):
    rel = p.relative_to(ROOT)
    if p.is_symlink(): errs.append(f'symlink forbidden: {rel}')
    if p.is_file() and (p.suffix.lower() in {'.zip','.tar','.gz','.7z','.rar','.pyc'} or '__pycache__' in p.parts or '.pytest_cache' in p.parts):
        errs.append(f'forbidden build artifact: {rel}')
    if p.is_file() and p.suffix.lower() in {'.md','.txt','.py','.json','.jsonl'}:
        text = p.read_text(encoding='utf-8', errors='ignore')
        if ('/mnt' + '/data/') in text or ('C:' + '\\Users\\') in text:
            errs.append(f'absolute build path leaked: {rel}')

core = (ROOT/'tools'/'catdistill.py').read_text(encoding='utf-8')
for term in ['requests','httpx','urllib.request','socket.create_connection','eval(','exec(']:
    if term in core: errs.append(f'core tool contains forbidden network/dynamic execution term: {term}')
try:
    with tempfile.TemporaryDirectory() as cd:
        py_compile.compile(str(ROOT/'tools'/'catdistill.py'), cfile=str(Path(cd)/'catdistill.pyc'), doraise=True)
except Exception as e:
    errs.append(f'core tool compile failed: {e}')

# Run commands on a temporary sample copy
with tempfile.TemporaryDirectory() as d:
    tmp = Path(d) / 'sample'
    shutil.copytree(ROOT/'examples'/'fictional_creator', tmp)
    cli = [sys.executable, str(ROOT/'tools'/'catdistill.py')]
    def run(args, expect=0):
        r = subprocess.run(cli + args, capture_output=True, text=True)
        if (r.returncode == 0) != (expect == 0):
            errs.append(f'command failed expectation: {args}; rc={r.returncode}; {r.stdout}{r.stderr}')
        return r
    run(['validate','--project',str(tmp)])
    for recipe in ['novel','screenplay','article','marketing']:
        run(['compile','--project',str(tmp),'--mode','MAKE','--recipe',recipe])
        run(['readiness','--project',str(tmp),'--mode','MAKE','--recipe',recipe])
    run(['compile','--project',str(tmp),'--mode','TALK','--recipe','article'])
    run(['make-trials','--project',str(tmp),'--recipe','novel'])
    safe = tmp/'compiled'/'safe_sample.txt'
    run(['leak-check','--project',str(tmp),'--text',str(safe)])
    copied = tmp/'compiled'/'positive_copy.txt'
    copied.write_text((tmp/'raw'/'novel_scene.txt').read_text(encoding='utf-8'), encoding='utf-8')
    r = subprocess.run(cli + ['leak-check','--project',str(tmp),'--text',str(copied)], capture_output=True, text=True)
    if r.returncode == 0: errs.append('positive leakage control was not detected')

# Full unit tests are run by the release pipeline outside this selfcheck.
# This avoids nested test runners while preserving deterministic package selfcheck.
if errs:
    print('SELF CHECK FAILED')
    for e in errs: print('- ' + e)
    raise SystemExit(1)
print('SELF CHECK PASSED')
print(f'root={ROOT}')
print(f'files={sum(1 for p in ROOT.rglob("*") if p.is_file())}')
print('quality_target=8/10')
print('network_access=none')
print('path_escape_guard=enabled')
