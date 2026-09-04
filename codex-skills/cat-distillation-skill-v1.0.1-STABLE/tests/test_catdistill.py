import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / 'tools' / 'catdistill.py'
SAMPLE = ROOT / 'examples' / 'fictional_creator'


def run(*args):
    return subprocess.run([sys.executable, str(CLI), *map(str, args)], capture_output=True, text=True)


def test_init_and_validate_empty():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'p'
        assert run('init', p).returncode == 0
        assert run('validate', '--project', p).returncode == 0


def test_hypothesis_cannot_be_active():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'p'; run('init', p)
        bad = {
            'id':'P1','jar':'CRAFT_JAR','trigger':'触发足够长','attention':'注意点','preference':'偏好点',
            'move':'执行动作足够长','visible_effect':'效果','boundaries':['边界'],'evidence_refs':['S1'],
            'support_level':'hypothesis','task_tags':['scene'],'source_tags':['novel'],'status':'active',
            'trial_refs':['T1'],'contrast_refs':['C1']
        }
        (p / 'pawprints.jsonl').write_text(json.dumps(bad, ensure_ascii=False) + '\n', encoding='utf-8')
        assert run('validate', '--project', p).returncode != 0


def test_active_needs_cleared_source():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'p'; run('init', p)
        raw = p / 'raw' / 'a.txt'; raw.write_text('sample', encoding='utf-8')
        import hashlib
        digest = hashlib.sha256(raw.read_bytes()).hexdigest()
        src = {'id':'SRC-1','path':'raw/a.txt','sha256':digest,'media_type':'txt','directness':'direct','authorization':'unknown','date':None,'tags':[],'notes':''}
        paw = {'id':'P1','jar':'CRAFT_JAR','trigger':'有明确场景任务','attention':'场景目标','preference':'先动作后解释','move':'让角色先行动再补信息','visible_effect':'场景更具体','boundaries':['教学说明除外'],'evidence_refs':['SRC-1'],'support_level':'medium','task_tags':['scene'],'source_tags':['novel'],'status':'active','trial_refs':['T1'],'contrast_refs':['C1']}
        (p / 'sources.jsonl').write_text(json.dumps(src, ensure_ascii=False) + '\n', encoding='utf-8')
        (p / 'pawprints.jsonl').write_text(json.dumps(paw, ensure_ascii=False) + '\n', encoding='utf-8')
        assert run('validate', '--project', p).returncode != 0


def test_path_escape_rejected():
    with tempfile.TemporaryDirectory() as d:
        base = Path(d); p = base / 'p'; run('init', p)
        outside = base / 'outside.txt'; outside.write_text('secret', encoding='utf-8')
        import hashlib
        src = {'id':'SRC-1','path':'../outside.txt','sha256':hashlib.sha256(outside.read_bytes()).hexdigest(),'media_type':'txt','directness':'direct','authorization':'cleared','date':None,'tags':[],'notes':''}
        (p / 'sources.jsonl').write_text(json.dumps(src, ensure_ascii=False) + '\n', encoding='utf-8')
        assert run('validate', '--project', p).returncode != 0


def test_compile_uses_active_only_and_has_quality_gate():
    r = run('compile','--project',SAMPLE,'--mode','MAKE','--recipe','novel')
    assert r.returncode == 0
    text = (SAMPLE / 'compiled' / 'make_novel.md').read_text(encoding='utf-8')
    assert '八分质量闸' in text
    assert 'PAW-005' not in text


def test_make_selection_not_voice_only():
    r = run('compile','--project',SAMPLE,'--mode','MAKE','--recipe','article')
    assert r.returncode == 0
    text = (SAMPLE / 'compiled' / 'make_article.md').read_text(encoding='utf-8')
    assert 'SENSE_JAR' in text or 'TASTE_JAR' in text or 'CRAFT_JAR' in text


def test_readiness_and_trial_generation():
    assert run('readiness','--project',SAMPLE,'--mode','MAKE','--recipe','novel').returncode == 0
    assert run('make-trials','--project',SAMPLE,'--recipe','novel').returncode == 0
    assert (SAMPLE / 'trials' / 'trial_arena_novel.md').exists()


def test_leak_check_positive_and_negative():
    safe = SAMPLE / 'compiled' / 'safe_sample.txt'
    assert run('leak-check','--project',SAMPLE,'--text',safe).returncode == 0
    copied = SAMPLE / 'compiled' / 'copied_for_test.txt'
    copied.write_text((SAMPLE / 'raw' / 'novel_scene.txt').read_text(encoding='utf-8'), encoding='utf-8')
    try:
        assert run('leak-check','--project',SAMPLE,'--text',copied).returncode != 0
    finally:
        copied.unlink(missing_ok=True)
