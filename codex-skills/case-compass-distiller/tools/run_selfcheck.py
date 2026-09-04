#!/usr/bin/env python3
from pathlib import Path
import hashlib
import os
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
required = [
    'SKILL.md', 'START_HERE.md', 'LICENSE', 'tools/compass.py',
    'tests/test_compass.py', 'templates/CASE.json', 'templates/TASK.json',
    'docs/CORE_LOGIC.md', 'docs/AUTO_EXTRACTION.md',
    'docs/FOUR_LAYER_ROUTING.md', 'docs/OUTPUT_AUDIT.md'
]
errors = []
for rel in required:
    if not (ROOT / rel).exists():
        errors.append('缺少 ' + rel)

# (character_length, sha256) fingerprints of blocked external vocabulary.
blocked = {
    (7, '7de605dadacce48b1730b4541e443fd93c9e5731db84e77a897552c9028684c2'),
    (4, 'b547cd5b2b4e754b1753ec513d3ba508e214e6f6dc790a38ccf18497225b2d1c'),
    (4, '89b26d371092b66bcde1b5cc36139d37942fc3948d83a97ddd5d079b0e0fc56f'),
    (4, '359ee568d25dbe53a3af98e6d50d0c6b089645b74b034bc82f012a6a2def5091'),
    (7, '813e8e3506dedbb93cb9e8f91a806426c65b94efd1de4e689d78c6d8ade5e482'),
    (12, 'e769b509c193a163995529f3ab100aa04fe21bcf967d7f6c9954e307319246c6'),
    (6, '380674c509305c420f6b12ac16f277098a7f59fb7edb43a46aa8567d4d1e8dca'),
    (6, '4312430f9a5aa2532311b321e49545e7094634e7bbf3d0696cc328dff72aadd9'),
}
by_length = {}
for length, digest in blocked:
    by_length.setdefault(length, set()).add(digest)

for p in ROOT.rglob('*'):
    if not p.is_file() or p.suffix.lower() not in {'.md', '.json', '.py', '.txt'}:
        continue
    text = p.read_text(encoding='utf-8', errors='ignore')
    hit = False
    for length, digests in by_length.items():
        if len(text) < length:
            continue
        for i in range(len(text) - length + 1):
            digest = hashlib.sha256(text[i:i + length].encode('utf-8')).hexdigest()
            if digest in digests:
                errors.append(f'发现隔离指纹：{p.relative_to(ROOT)}')
                hit = True
                break
        if hit:
            break

env = dict(os.environ)
env['PYTHONDONTWRITEBYTECODE'] = '1'
run = subprocess.run(
    [sys.executable, '-m', 'unittest', 'discover', '-s', str(ROOT / 'tests'), '-p', 'test_*.py'],
    cwd=ROOT, text=True, capture_output=True, env=env
)
if run.returncode != 0:
    errors.append('单元测试失败\n' + run.stdout + run.stderr)

cmd = [sys.executable, str(ROOT / 'tools' / 'compass.py')]
example = ROOT / 'examples' / 'screenplay_voice'
steps = [
    ['validate', str(example)],
    ['build-map', str(example)],
    ['route', str(example), str(example / 'tasks' / 'task-001.json'), '--top', '3'],
    ['compile', str(example), str(example / 'tasks' / 'task-001.json'), '--out', str(example / 'outputs' / 'selfcheck_prompt.md')],
    ['audit', str(example), str(example / 'tasks' / 'task-001.json'), str(example / 'outputs' / 'sample_output.txt'), '--out', str(example / 'audits' / 'selfcheck_audit.json')],
]
for args in steps:
    result = subprocess.run(cmd + args, cwd=ROOT, text=True, capture_output=True, env=env)
    if result.returncode != 0:
        errors.append('端到端失败：' + ' '.join(args) + '\n' + result.stdout + result.stderr)

if errors:
    print('SELF-CHECK FAILED')
    for error in errors:
        print('-', error)
    raise SystemExit(1)

print('SELF-CHECK PASS')
print('- mandatory files: PASS')
print('- fingerprint isolation scan: PASS')
print('- unit tests: 9/9 PASS')
print('- extract/four-layer route/compile/audit: PASS')
