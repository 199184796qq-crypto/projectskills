#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

TEXT_EXTS = {'.txt':'txt','.md':'md','.json':'json','.csv':'csv','.srt':'srt','.vtt':'vtt'}
JARS = {'SENSE_JAR','TASTE_JAR','CRAFT_JAR','VOICE_JAR','RELATION_JAR'}
STATUSES = {'candidate','tested','active','retired'}
LEVELS = {'strong','medium','weak','hypothesis'}
MODES = {'MAKE','REWORK','PLAN','TALK'}
RECIPES = {'novel','screenplay','article','marketing'}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read_jsonl(path: Path):
    if not path.exists():
        return []
    out = []
    for no, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if line.strip():
            try:
                out.append(json.loads(line))
            except Exception as e:
                raise ValueError(f'{path}:{no}: {e}')
    return out


def write_jsonl(path: Path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + ('\n' if rows else ''), encoding='utf-8')


def safe_project_path(project: Path, relative: str, must_exist: bool = True) -> Path:
    base = project.resolve()
    rel = Path(relative)
    if rel.is_absolute():
        raise ValueError(f'absolute path is forbidden: {relative}')
    candidate = (base / rel).resolve(strict=False)
    try:
        candidate.relative_to(base)
    except ValueError:
        raise ValueError(f'path escapes project directory: {relative}')
    if must_exist and not candidate.exists():
        raise ValueError(f'path does not exist: {relative}')
    if candidate.exists() and candidate.is_symlink():
        raise ValueError(f'symlink source is forbidden: {relative}')
    return candidate


def load_recipe(name: str) -> dict:
    path = Path(__file__).resolve().parents[1] / 'recipes' / f'{name}.json'
    if not path.exists():
        raise SystemExit(f'unknown recipe: {name}')
    return json.loads(path.read_text(encoding='utf-8'))


def init_project(project: Path):
    project.mkdir(parents=True, exist_ok=True)
    for d in ['raw', 'corpus', 'compiled', 'reports', 'trials']:
        (project / d).mkdir(exist_ok=True)
    card = {
        'project_name': project.name,
        'skill_version': '1.0.1',
        'delivery_level': 'practical-strong',
        'quality_target': 8,
        'subject_label': '',
        'purpose': [],
        'allowed_materials': [],
        'forbidden_uses': [],
        'target_outputs': ['novel', 'screenplay', 'article', 'marketing', 'collaboration'],
        'authorization_note': '',
        'created_at': ''
    }
    (project / 'project.json').write_text(json.dumps(card, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    for f in ['sources.jsonl', 'pawprints.jsonl', 'feedback.jsonl', 'trials.jsonl']:
        (project / f).touch()
    print(f'initialized: {project}')


def scan_corpus(source: Path, project: Path):
    if not (project / 'project.json').exists():
        raise SystemExit('project not initialized')
    if source.is_symlink():
        raise SystemExit('symlink source directory is forbidden')
    rows = read_jsonl(project / 'sources.jsonl')
    known = {r.get('sha256') for r in rows}
    added = 0
    for p in sorted(source.rglob('*')):
        if not p.is_file() or p.is_symlink():
            continue
        digest = sha256(p)
        if digest in known:
            continue
        ext = p.suffix.lower()
        media = TEXT_EXTS.get(ext, 'other')
        target = project / 'raw' / f'{digest[:12]}_{p.name}'
        shutil.copy2(p, target)
        row = {
            'id': f'SRC-{len(rows)+1:04d}',
            'path': str(target.relative_to(project)),
            'sha256': digest,
            'media_type': media,
            'directness': 'unknown',
            'authorization': 'unknown',
            'date': None,
            'tags': [],
            'notes': f'imported from {p.name}'
        }
        rows.append(row)
        known.add(digest)
        added += 1
    write_jsonl(project / 'sources.jsonl', rows)
    print(f'scanned: {added} new files, {len(rows)} total')


def validate_paw(p, idx):
    req = ['id','jar','trigger','attention','preference','move','visible_effect','boundaries','evidence_refs','support_level','task_tags','source_tags','status']
    errs = []
    for k in req:
        if k not in p or p[k] in ('', None, []):
            errs.append(f'#{idx} missing {k}')
    if p.get('jar') not in JARS:
        errs.append(f'#{idx} invalid jar')
    if p.get('status') not in STATUSES:
        errs.append(f'#{idx} invalid status')
    if p.get('support_level') not in LEVELS:
        errs.append(f'#{idx} invalid support_level')
    if p.get('status') in {'tested','active'} and p.get('support_level') == 'hypothesis':
        errs.append(f'#{idx} hypothesis cannot be tested/active')
    if p.get('status') == 'active' and len(p.get('evidence_refs', [])) < 2 and len(p.get('trial_refs', [])) < 1:
        errs.append(f'#{idx} active needs two evidence refs or one successful trial')
    if p.get('status') in {'tested','active'} and len(p.get('contrast_refs', [])) < 1:
        errs.append(f'#{idx} tested/active without contrast attack')
    if p.get('max_uses_per_output') is not None and not (1 <= int(p['max_uses_per_output']) <= 5):
        errs.append(f'#{idx} invalid max_uses_per_output')
    return errs


def source_map(project: Path):
    return {s.get('id'): s for s in read_jsonl(project / 'sources.jsonl')}


def validate_project(project: Path):
    errs = []
    for f in ['project.json','sources.jsonl','pawprints.jsonl','feedback.jsonl']:
        if not (project / f).exists():
            errs.append(f'missing {f}')
    if errs:
        print('\n'.join(errs))
        return 1
    sources = read_jsonl(project / 'sources.jsonl')
    smap = {s.get('id'): s for s in sources}
    for i, s in enumerate(sources, 1):
        try:
            p = safe_project_path(project, s.get('path', ''))
        except ValueError as e:
            errs.append(f'source #{i}: {e}')
            continue
        if s.get('sha256') != sha256(p):
            errs.append(f'source #{i} hash mismatch')
    paws = read_jsonl(project / 'pawprints.jsonl')
    ids = set()
    for i, p in enumerate(paws, 1):
        errs += validate_paw(p, i)
        if p.get('id') in ids:
            errs.append(f'duplicate pawprint id {p.get("id")}')
        ids.add(p.get('id'))
        if p.get('status') in {'tested','active'}:
            for ref in p.get('evidence_refs', []):
                if ref not in smap:
                    errs.append(f'#{i} unknown evidence source {ref}')
                elif smap[ref].get('authorization') != 'cleared':
                    errs.append(f'#{i} evidence {ref} is not cleared')
    active = [p for p in paws if p.get('status') == 'active']
    report = {
        'sources': len(sources),
        'pawprints': len(paws),
        'active': len(active),
        'jar_counts': {j: sum(1 for p in active if p.get('jar') == j) for j in sorted(JARS)}
    }
    (project / 'reports').mkdir(exist_ok=True)
    (project / 'reports' / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if errs:
        print('VALIDATION FAILED')
        print('\n'.join('- ' + e for e in errs))
        return 1
    print('VALIDATION PASSED')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


def eligible_pawprints(project: Path):
    smap = source_map(project)
    out = []
    for p in read_jsonl(project / 'pawprints.jsonl'):
        if p.get('status') != 'active' or p.get('support_level') == 'hypothesis':
            continue
        refs = p.get('evidence_refs', [])
        if not refs or any(r not in smap or smap[r].get('authorization') != 'cleared' for r in refs):
            continue
        out.append(p)
    return out


def mode_jars(mode: str, recipe: dict):
    if mode == 'TALK':
        return ['RELATION_JAR','VOICE_JAR'], ['TASTE_JAR']
    if mode == 'REWORK':
        return ['TASTE_JAR','CRAFT_JAR'], ['VOICE_JAR','RELATION_JAR']
    if mode == 'PLAN':
        return ['SENSE_JAR','TASTE_JAR','CRAFT_JAR'], []
    return recipe.get('required_jars', ['SENSE_JAR','TASTE_JAR','CRAFT_JAR']), recipe.get('optional_jars', ['VOICE_JAR'])


def paw_score(p: dict, preferred_tags: set, wanted_jars: set):
    overlap = len(preferred_tags.intersection(p.get('task_tags', [])))
    level = {'strong': 4, 'medium': 3, 'weak': 1}.get(p.get('support_level'), 0)
    jar_bonus = 4 if p.get('jar') in wanted_jars else 0
    return overlap * 10 + level + jar_bonus


def select_pawprints(project: Path, mode: str, recipe: dict):
    paws = eligible_pawprints(project)
    required, optional = mode_jars(mode, recipe)
    preferred = set(recipe.get('preferred_tags', []))
    max_total = int(recipe.get('max_pawprints', 7))
    max_voice = int(recipe.get('max_voice', 2))
    selected = []
    used = set()

    def candidates_for(jar):
        return sorted(
            [p for p in paws if p.get('jar') == jar and p.get('id') not in used],
            key=lambda p: (paw_score(p, preferred, set(required + optional)), p.get('id','')),
            reverse=True
        )

    for jar in required:
        c = candidates_for(jar)
        if c:
            selected.append(c[0]); used.add(c[0]['id'])
    remaining = sorted(
        [p for p in paws if p.get('id') not in used and p.get('jar') in set(required + optional)],
        key=lambda p: (paw_score(p, preferred, set(required + optional)), p.get('id','')),
        reverse=True
    )
    for p in remaining:
        if len(selected) >= max_total:
            break
        if p.get('jar') == 'VOICE_JAR' and sum(1 for x in selected if x.get('jar') == 'VOICE_JAR') >= max_voice:
            continue
        selected.append(p); used.add(p['id'])
    gaps = [j for j in required if not any(p.get('jar') == j for p in selected)]
    return selected, gaps


def compile_prompt(project: Path, mode: str, recipe_name: str, out: Path | None):
    recipe = load_recipe(recipe_name)
    selected, gaps = select_pawprints(project, mode, recipe)
    lines = [
        '# 猫咪蒸馏运行包',
        f'- 模式：{mode}',
        f'- 食谱：{recipe_name}',
        '- 目标：稳定完成任务，正式输出须通过八分质量闸。',
        '',
        '## 必要任务槽位'
    ]
    lines += [f'- {x}' for x in recipe['required_slots']]
    lines += ['', '## 建造顺序']
    lines += [f'{i}. {x}' for i, x in enumerate(recipe.get('build_order', []), 1)]
    lines += ['', '## 已验证爪印']
    if not selected:
        lines += ['- 当前没有可用且授权清楚的活动爪印。必须执行空槽协议，不得脑补个人特征。']
    for p in selected:
        lines += [
            f"### {p['id']}｜{p['jar']}",
            f"触发：{p['trigger']}",
            f"注意：{p['attention']}",
            f"偏好：{p['preference']}",
            f"动作：{p['move']}",
            f"效果：{p['visible_effect']}",
            '边界：' + '；'.join(p['boundaries']),
            f"单篇上限：{p.get('max_uses_per_output', '按原密度保守使用')}",
            f"替代动作：{p.get('fallback_move') or '触发不成立时使用中性工艺，不强行模仿'}",
            ''
        ]
    lines += ['## 空槽']
    if gaps:
        lines += [f'- 缺少 {j} 的活动证据：使用中性工艺并显式标注，不得补人格。' for j in gaps]
    else:
        lines += ['- 本次要求的核心罐均有覆盖。']
    lines += ['', '## 交付前质量检查']
    lines += [f'- {x}' for x in recipe.get('quality_checks', [])]
    lines += [
        '- 按任务完成度、具体性、爪印匹配、自然度、安全与泄漏五项各0—2分；总分不足8分不得交付。',
        '- 完成后检查刻板化、语料偏斜、上下文坍缩、通用工艺冒名与原文拼贴。',
        '- 不得声称代表本人、复制完整人格或拥有材料之外的私人知识。'
    ]
    text = '\n'.join(lines) + '\n'
    out = out or project / 'compiled' / f'{mode.lower()}_{recipe_name}.md'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding='utf-8')
    print(out)


def nutrition_report(project: Path):
    sources = read_jsonl(project / 'sources.jsonl')
    paws = read_jsonl(project / 'pawprints.jsonl')
    active = [p for p in paws if p.get('status') == 'active']
    directness, media = {}, {}
    unknown_auth = restricted = 0
    for s in sources:
        directness[s.get('directness','unknown')] = directness.get(s.get('directness','unknown'),0) + 1
        media[s.get('media_type','other')] = media.get(s.get('media_type','other'),0) + 1
        if s.get('authorization') == 'unknown': unknown_auth += 1
        if s.get('authorization') == 'restricted': restricted += 1
    jars = {j: sum(1 for p in active if p.get('jar') == j) for j in sorted(JARS)}
    warnings = []
    if active and jars.get('VOICE_JAR',0) / len(active) > 0.5:
        warnings.append('voice-heavy: project may be expression-only')
    if unknown_auth:
        warnings.append(f'{unknown_auth} sources have unknown authorization')
    if restricted:
        warnings.append(f'{restricted} sources are restricted and cannot feed active pawprints')
    if not active:
        warnings.append('no active pawprints')
    if sum(1 for x in jars.values() if x > 0) < 3:
        warnings.append('fewer than three jars have active coverage')
    report = {
        'source_count': len(sources), 'media_types': media, 'directness': directness,
        'unknown_authorization': unknown_auth, 'restricted_authorization': restricted,
        'pawprint_count': len(paws), 'active_pawprints': len(active),
        'active_jar_counts': jars, 'warnings': warnings
    }
    out = project / 'reports' / 'nutrition.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def readiness_report(project: Path, mode: str, recipe_name: str):
    recipe = load_recipe(recipe_name)
    selected, gaps = select_pawprints(project, mode, recipe)
    sources = source_map(project)
    active = eligible_pawprints(project)
    trials = read_jsonl(project / 'trials.jsonl')
    passed_trials = sum(1 for t in trials if t.get('result') == 'pass' and (t.get('recipe') in (None, recipe_name)))
    scores = {
        'evidence': 2 if len(active) >= 4 else (1 if len(active) >= 2 else 0),
        'coverage': 2 if not gaps else (1 if len(gaps) == 1 else 0),
        'trials': 2 if passed_trials >= 2 else (1 if passed_trials == 1 else 0),
        'safety': 2 if all(s.get('authorization') == 'cleared' for s in sources.values()) else 1,
        'balance': 2 if selected and sum(1 for p in selected if p.get('jar') == 'VOICE_JAR') <= 2 else (1 if selected else 0)
    }
    total = sum(scores.values())
    status = 'ready' if total >= 8 and scores['safety'] == 2 else ('limited' if total >= 6 else 'not-ready')
    report = {
        'mode': mode, 'recipe': recipe_name, 'status': status, 'score': total,
        'scores': scores, 'selected_pawprints': [p['id'] for p in selected],
        'missing_jars': gaps,
        'note': 'score is a practical readiness gate, not a claim of full identity replication'
    }
    out = project / 'reports' / f'readiness_{mode.lower()}_{recipe_name}.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def make_trials(project: Path, recipe_name: str):
    recipe = load_recipe(recipe_name)
    selected, gaps = select_pawprints(project, 'MAKE', recipe)
    ids = [p['id'] for p in selected[:5]]
    text = f'''# 三次试爪｜{recipe_name}\n\n## 第一爪：同类任务\n\n使用爪印：{', '.join(ids) or '无，先补证据'}\n\n要求：完成一个不超过800字或两页的同类任务，重点检查任务完成、手艺动作与声音密度。\n\n## 第二爪：邻近迁移\n\n使用同一组核心爪印，换一个相邻题材或场景。不得沿用原文情节、句子和罕见比喻。\n\n## 第三爪：改稿与协作\n\n给一段存在重复解释、结构松散或目标不清的文本，先说明问题，再做局部修正。\n\n## 评分\n\n每题按五项各0—2分：任务完成、具体性、爪印匹配、自然度、安全与泄漏。总分至少8分且安全项必须2分。\n\n## 当前空槽\n\n{'; '.join(gaps) if gaps else '核心罐覆盖完整。'}\n'''
    out = project / 'trials' / f'trial_arena_{recipe_name}.md'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding='utf-8')
    print(out)


def normalize_text(s: str) -> str:
    return re.sub(r'\s+', '', s)


def leak_check(project: Path, text_path: Path, n: int = 12):
    target = normalize_text(text_path.read_text(encoding='utf-8', errors='ignore'))
    matches = []
    for s in read_jsonl(project / 'sources.jsonl'):
        try:
            p = safe_project_path(project, s['path'])
        except ValueError:
            continue
        if p.suffix.lower() not in TEXT_EXTS:
            continue
        src = normalize_text(p.read_text(encoding='utf-8', errors='ignore'))
        seen = set()
        for i in range(max(0, len(src) - n + 1)):
            gram = src[i:i+n]
            if len(gram) == n and gram in target and gram not in seen:
                seen.add(gram)
                matches.append({'source': s['id'], 'fragment': gram})
                if len(matches) >= 50:
                    break
    report = {'n': n, 'matches': matches, 'risk': 'high' if matches else 'clear'}
    out = project / 'reports' / 'leakage.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 2 if matches else 0


def audit_project(project: Path):
    validation = validate_project(project)
    nutrition_report(project)
    readiness = [readiness_report(project, 'MAKE', r) for r in sorted(RECIPES)]
    talk = readiness_report(project, 'TALK', 'article')
    summary = {
        'validation': 'pass' if validation == 0 else 'fail',
        'make_readiness': {r['recipe']: r['status'] for r in readiness},
        'talk_readiness': talk['status']
    }
    out = project / 'reports' / 'strict_audit.json'
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 1 if validation else 0


def main():
    ap = argparse.ArgumentParser(prog='catdistill')
    sp = ap.add_subparsers(dest='cmd', required=True)
    p = sp.add_parser('init'); p.add_argument('project', type=Path)
    p = sp.add_parser('scan'); p.add_argument('source', type=Path); p.add_argument('--project', required=True, type=Path)
    p = sp.add_parser('validate'); p.add_argument('--project', required=True, type=Path)
    p = sp.add_parser('compile'); p.add_argument('--project', required=True, type=Path); p.add_argument('--mode', choices=sorted(MODES), default='MAKE'); p.add_argument('--recipe', choices=sorted(RECIPES), default='novel'); p.add_argument('--out', type=Path)
    p = sp.add_parser('nutrition'); p.add_argument('--project', required=True, type=Path)
    p = sp.add_parser('readiness'); p.add_argument('--project', required=True, type=Path); p.add_argument('--mode', choices=sorted(MODES), default='MAKE'); p.add_argument('--recipe', choices=sorted(RECIPES), default='novel')
    p = sp.add_parser('make-trials'); p.add_argument('--project', required=True, type=Path); p.add_argument('--recipe', choices=sorted(RECIPES), default='novel')
    p = sp.add_parser('leak-check'); p.add_argument('--project', required=True, type=Path); p.add_argument('--text', required=True, type=Path); p.add_argument('--ngram', type=int, default=12)
    p = sp.add_parser('audit'); p.add_argument('--project', required=True, type=Path)
    a = ap.parse_args()
    if a.cmd == 'init': init_project(a.project)
    elif a.cmd == 'scan': scan_corpus(a.source, a.project)
    elif a.cmd == 'validate': raise SystemExit(validate_project(a.project))
    elif a.cmd == 'compile': compile_prompt(a.project, a.mode, a.recipe, a.out)
    elif a.cmd == 'nutrition': nutrition_report(a.project)
    elif a.cmd == 'readiness': readiness_report(a.project, a.mode, a.recipe)
    elif a.cmd == 'make-trials': make_trials(a.project, a.recipe)
    elif a.cmd == 'leak-check': raise SystemExit(leak_check(a.project, a.text, a.ngram))
    elif a.cmd == 'audit': raise SystemExit(audit_project(a.project))


if __name__ == '__main__':
    main()
