#!/usr/bin/env python3
"""Case Compass Distiller 1.1 - local precedent routing, standard-library only."""
from __future__ import annotations
import argparse, hashlib, json, math, re, sys
from pathlib import Path
from datetime import date
from statistics import mean, pstdev
from typing import Any, Dict, List, Tuple

REQUIRED_CASE = ["id", "title", "status", "coordinates", "case_map", "slices", "fingerprint", "evidence", "source"]
REQUIRED_TASK = ["id", "title", "coordinates", "input"]
LAYERS = ("structure", "voice", "dialogue", "interaction")

GUIDE = """案例罗盘蒸馏 1.1｜上手六步
1. 说清要学会的具体任务。
2. 放入 3—12 个你认可的案例原文。
3. 用 extract 自动建卡；必要时只修正观察结果。
4. 用 build-map 建立局部案例地图。
5. 用 compile 为新任务生成四层迁移提示。
6. 完成后用 audit 检查接近度、硬要求与原句重叠。

本工具不建立人格模型，不宣布通用规则；它只在局部案例附近做导航和迁移。
"""

PUNCT_RE = re.compile(r"[，。！？；：,.!?;:]")
SENT_RE = re.compile(r"(?<=[。！？!?])|\n+")
SPEAKER_RE = re.compile(r"^\s*([^：:\n]{1,18})[：:]\s*(.+)$")


def load(path: Path) -> Dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"文件不存在：{path}")
    except json.JSONDecodeError as e:
        raise SystemExit(f"JSON 无法解析：{path}｜{e}")


def dump(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def require(obj: Dict[str, Any], fields: List[str], label: str) -> List[str]:
    return [f"{label} 缺少字段：{x}" for x in fields if x not in obj]


def clean_text(text: str) -> str:
    return re.sub(r"\s+", "", text or "")


def split_sentences(text: str) -> List[str]:
    return [x.strip() for x in SENT_RE.split(text or "") if x.strip()]


def round4(x: float) -> float:
    return round(float(x), 4)


def ratio(n: float, d: float) -> float:
    return round4(n / d) if d else 0.0


def text_fingerprint(text: str) -> Dict[str, Any]:
    raw = text or ""
    compact = clean_text(raw)
    chars = max(1, len(compact))
    sents = split_sentences(raw)
    slens = [len(clean_text(s)) for s in sents if clean_text(s)] or [chars]
    paras = [p.strip() for p in re.split(r"\n\s*\n|\n", raw) if p.strip()]
    plens = [len(clean_text(p)) for p in paras] or [chars]
    lines = [x.strip() for x in raw.splitlines() if x.strip()]
    dialogue_lines = []
    speakers = []
    for line in lines:
        m = SPEAKER_RE.match(line)
        if m:
            speakers.append(m.group(1).strip())
            dialogue_lines.append(m.group(2).strip())
    quote_marks = sum(raw.count(x) for x in ['“','”','「','」','『','』','\"'])
    q = raw.count('？') + raw.count('?')
    ex = raw.count('！') + raw.count('!')
    dash = raw.count('——') + raw.count('—')
    ell = raw.count('……') + raw.count('...')
    avg_s = mean(slens)
    cv = pstdev(slens) / avg_s if len(slens) > 1 and avg_s else 0.0
    avg_turn = mean([len(clean_text(x)) for x in dialogue_lines]) if dialogue_lines else 0.0
    alternations = sum(1 for a,b in zip(speakers, speakers[1:]) if a != b)
    alt_ratio = ratio(alternations, max(1, len(speakers)-1)) if speakers else 0.0
    if avg_s <= 14: sentence_band = "short"
    elif avg_s <= 26: sentence_band = "medium"
    else: sentence_band = "long"
    rhythm = "varied" if cv >= .65 else "steady" if cv <= .28 else "mixed"
    dialogue_density = "high" if len(dialogue_lines) >= max(3, len(lines)*.45) else "medium" if dialogue_lines else "low"
    return {
        "sha256": hashlib.sha256(raw.encode('utf-8')).hexdigest(),
        "char_count": len(compact),
        "sentence_count": len(slens),
        "paragraph_count": len(paras),
        "avg_sentence_chars": round4(avg_s),
        "sentence_length_cv": round4(cv),
        "avg_paragraph_chars": round4(mean(plens)),
        "question_rate": ratio(q*100, chars),
        "exclaim_rate": ratio(ex*100, chars),
        "dash_rate": ratio(dash*100, chars),
        "ellipsis_rate": ratio(ell*100, chars),
        "quote_mark_rate": ratio(quote_marks*100, chars),
        "dialogue_turn_count": len(dialogue_lines),
        "avg_dialogue_turn_chars": round4(avg_turn),
        "speaker_count": len(set(speakers)),
        "speaker_alternation": alt_ratio,
        "sentence_band": sentence_band,
        "rhythm_shape": rhythm,
        "dialogue_density": dialogue_density
    }


def observed_slices(fp: Dict[str, Any]) -> Dict[str, Any]:
    pc = fp.get('paragraph_count', 1)
    if pc <= 1: phases = ["single_block"]
    elif pc == 2: phases = ["opening", "payoff"]
    elif pc == 3: phases = ["opening", "development", "payoff"]
    else: phases = ["opening", "development", "change", "payoff"]
    voice_marks = [
        f"sentence_band={fp.get('sentence_band')}",
        f"rhythm={fp.get('rhythm_shape')}",
        f"questions_per_100={fp.get('question_rate')}",
        f"exclaims_per_100={fp.get('exclaim_rate')}",
        f"ellipsis_per_100={fp.get('ellipsis_rate')}"
    ]
    dialogue_marks = [
        f"density={fp.get('dialogue_density')}",
        f"turns={fp.get('dialogue_turn_count')}",
        f"avg_turn_chars={fp.get('avg_dialogue_turn_chars')}"
    ]
    interaction_marks = [
        f"speakers={fp.get('speaker_count')}",
        f"alternation={fp.get('speaker_alternation')}",
        "reaction_order=source_observation_required"
    ]
    return {
        "structure": {
            "phase_slots": phases,
            "paragraph_count": pc,
            "pace_observation": f"avg_paragraph_chars={fp.get('avg_paragraph_chars')}",
            "turn_observation": "manual_review_recommended"
        },
        "voice": {
            "observable_marks": voice_marks,
            "sentence_band": fp.get('sentence_band'),
            "rhythm_shape": fp.get('rhythm_shape'),
            "manual_notes": []
        },
        "dialogue": {
            "observable_marks": dialogue_marks,
            "dialogue_density": fp.get('dialogue_density'),
            "manual_notes": []
        },
        "interaction": {
            "observable_marks": interaction_marks,
            "speaker_count": fp.get('speaker_count'),
            "manual_notes": []
        }
    }


def init_project(path: Path, name: str) -> None:
    path.mkdir(parents=True, exist_ok=True)
    for d in ["cases", "tasks", "outputs", "results", "sources", "audits"]:
        (path / d).mkdir(exist_ok=True)
    project = {
        "project_id": path.name,
        "name": name,
        "ability_goal": "待填写",
        "success_definition": ["任务完成", "可以直接使用"],
        "created_at": date.today().isoformat(),
        "version": 2
    }
    dump(path / "project.json", project)
    print(f"已建立案例罗盘项目：{path}")
    print("下一步：把案例原文放入 sources，然后运行 extract。")


def auto_case_from_source(source_file: Path, args: argparse.Namespace) -> Dict[str, Any]:
    text = source_file.read_text(encoding='utf-8')
    fp = text_fingerprint(text)
    slices = observed_slices(fp)
    constraints = [x.strip() for x in (args.constraints or '').split(',') if x.strip()]
    tones = [x.strip() for x in (args.tone or '').split(',') if x.strip()]
    return {
        "id": args.id,
        "title": args.title,
        "status": args.status,
        "coordinates": {
            "domain": args.domain,
            "job": args.job,
            "format": args.format,
            "audience": args.audience,
            "length": fp['char_count'],
            "tone": tones,
            "constraints": constraints
        },
        "case_map": {
            "starting_state": args.starting_state or "source_case",
            "ending_state": args.ending_state or "observed_success_output",
            "path": slices['structure']['phase_slots'],
            "must_keep": ["保留本案例已观察到的结构关系，不复制具体措辞"],
            "replaceable": ["题材、人物、事实、数据和全部具体表达"],
            "avoid": ["长句复刻", "把单个案例当作普遍结论"]
        },
        "slices": slices,
        "fingerprint": fp,
        "evidence": {
            "why_successful": args.why_successful or "待用户补充",
            "proof_type": args.proof_type,
            "score": args.score,
            "layer_confidence": {"structure": .72, "voice": .68, "dialogue": .66, "interaction": .62}
        },
        "source": {"path": str(source_file), "authorized": True, "sha256": fp['sha256']},
        "limits": ["自动建卡只提供可观察特征；语义与剧情功能建议人工复核"]
    }


def extract_case(project: Path, source_file: Path, args: argparse.Namespace) -> None:
    if not source_file.exists(): raise SystemExit(f"原文不存在：{source_file}")
    target_source = project / 'sources' / f"{args.id}{source_file.suffix or '.txt'}"
    target_source.write_text(source_file.read_text(encoding='utf-8'), encoding='utf-8')
    case = auto_case_from_source(target_source, args)
    target = project / 'cases' / f"{case['id']}.json"
    dump(target, case)
    print(f"已自动建卡：{case['id']}｜{case['title']}")
    print(f"四层切片：structure / voice / dialogue / interaction")


def validate_case(case: Dict[str, Any]) -> List[str]:
    errors = require(case, REQUIRED_CASE, f"案例 {case.get('id','?')}")
    if errors: return errors
    c = case.get("coordinates", {})
    for key in ["domain", "job", "format", "audience", "length", "tone", "constraints"]:
        if key not in c: errors.append(f"案例 {case['id']} coordinates 缺少：{key}")
    m = case.get("case_map", {})
    for key in ["starting_state", "ending_state", "path", "must_keep", "replaceable", "avoid"]:
        if key not in m: errors.append(f"案例 {case['id']} case_map 缺少：{key}")
    for layer in LAYERS:
        if layer not in case.get('slices', {}): errors.append(f"案例 {case['id']} slices 缺少：{layer}")
    if 'sha256' not in case.get('fingerprint', {}): errors.append(f"案例 {case['id']} fingerprint 缺少 sha256")
    if case.get("status") not in {"success","failure","draft"}: errors.append(f"案例 {case['id']} status 非法")
    return errors


def validate_task(task: Dict[str, Any]) -> List[str]:
    errors = require(task, REQUIRED_TASK, f"任务 {task.get('id','?')}")
    if errors: return errors
    c = task.get("coordinates", {})
    for key in ["domain", "job", "format", "audience", "length", "tone", "constraints"]:
        if key not in c: errors.append(f"任务 {task['id']} coordinates 缺少：{key}")
    return errors


def add_case(project: Path, case_file: Path) -> None:
    case = load(case_file)
    errors = validate_case(case)
    if errors: raise SystemExit("\n".join(errors))
    dump(project / "cases" / f"{case['id']}.json", case)
    print(f"已加入案例：{case['id']}｜{case['title']}")


def list_cases(project: Path, successes_only: bool=False) -> List[Dict[str, Any]]:
    cases=[]
    for p in sorted((project / "cases").glob("*.json")):
        c=load(p)
        if successes_only and c.get("status") != "success": continue
        cases.append(c)
    return cases


def build_map(project: Path) -> Dict[str, Any]:
    cases=list_cases(project)
    neighborhoods: Dict[str, List[str]] = {}
    for c in cases:
        x=c["coordinates"]
        key=f"{x.get('domain','?')}::{x.get('job','?')}::{x.get('format','?')}"
        neighborhoods.setdefault(key, []).append(c["id"])
    data={
        "project": project.name,
        "case_count": len(cases),
        "success_count": sum(1 for c in cases if c.get("status")=="success"),
        "failure_count": sum(1 for c in cases if c.get("status")=="failure"),
        "neighborhoods": neighborhoods,
        "layer_readiness": {layer: sum(1 for c in cases if c.get('slices',{}).get(layer)) for layer in LAYERS}
    }
    dump(project / "case_map.json", data)
    print(f"案例地图已生成：{len(cases)} 个案例，{len(neighborhoods)} 个邻域")
    return data


def jaccard(a: List[str], b: List[str]) -> float:
    sa, sb = set(map(str,a or [])), set(map(str,b or []))
    if not sa and not sb: return 1.0
    if not sa or not sb: return 0.0
    return len(sa & sb) / len(sa | sb)


def exact(a: Any,b: Any) -> float:
    return 1.0 if str(a).strip().lower()==str(b).strip().lower() else 0.0


def length_fit(a: Any,b: Any) -> float:
    try:
        a=float(a); b=float(b)
        if a<=0 or b<=0: return 0.0
        return max(0.0, 1.0 - abs(a-b)/max(a,b))
    except Exception: return 0.0


def quality(case: Dict[str, Any], layer: str) -> float:
    q=float(case.get("evidence",{}).get("score",8.0) or 8.0)
    conf=float(case.get('evidence',{}).get('layer_confidence',{}).get(layer,.65))
    return max(.55, min(1.0, (q/10.0)*(.65+.35*conf)))


def layer_score(case: Dict[str, Any], task: Dict[str, Any], layer: str) -> float:
    c,t=case["coordinates"],task["coordinates"]
    weights={
        'structure': [(4,exact(c.get('job'),t.get('job'))),(3,exact(c.get('format'),t.get('format'))),(2,exact(c.get('domain'),t.get('domain'))),(1.5,length_fit(c.get('length'),t.get('length'))),(1,jaccard(c.get('constraints',[]),t.get('constraints',[])))],
        'voice': [(3,jaccard(c.get('tone',[]),t.get('tone',[]))),(2.5,exact(c.get('audience'),t.get('audience'))),(2,exact(c.get('format'),t.get('format'))),(1.5,length_fit(c.get('length'),t.get('length'))),(1,exact(c.get('domain'),t.get('domain')))],
        'dialogue': [(3,exact(c.get('format'),t.get('format'))),(2.5,exact(c.get('job'),t.get('job'))),(2,jaccard(c.get('tone',[]),t.get('tone',[]))),(1.5,exact(c.get('audience'),t.get('audience'))),(1,jaccard(c.get('constraints',[]),t.get('constraints',[])))],
        'interaction': [(3,exact(c.get('job'),t.get('job'))),(2.5,exact(c.get('format'),t.get('format'))),(2,jaccard(c.get('constraints',[]),t.get('constraints',[]))),(1.5,exact(c.get('domain'),t.get('domain'))),(1,exact(c.get('audience'),t.get('audience')))]
    }[layer]
    return round4(sum(w*s for w,s in weights)/sum(w for w,_ in weights)*quality(case,layer))


def overall_score(case: Dict[str, Any], task: Dict[str, Any]) -> float:
    return round4(sum(layer_score(case,task,x) for x in LAYERS)/len(LAYERS))


def differences(case: Dict[str, Any], task: Dict[str, Any]) -> Dict[str, Any]:
    c,t=case["coordinates"],task["coordinates"]
    changed={}
    for key in ["domain","job","format","audience","length","tone","constraints"]:
        if c.get(key)!=t.get(key): changed[key]={"from":c.get(key),"to":t.get(key)}
    cm=case.get("case_map",{})
    tc=set(map(str,t.get("constraints",[]) or [])); cc=set(map(str,c.get("constraints",[]) or []))
    watch=list(cm.get("avoid",[]))
    if changed: watch.append("只迁移观察到的关系，不携带领航案例的题材和原句")
    return {
        "KEEP": cm.get("must_keep",[]) or cm.get("path",[])[:2],
        "REPLACE": cm.get("replaceable",[]),
        "ADD": sorted(tc-cc),
        "REMOVE": sorted(cc-tc),
        "WATCH": watch,
        "coordinate_changes": changed
    }


def fit_label(score: float) -> str:
    return "GOOD_FIT" if score>=.72 else "PARTIAL_FIT" if score>=.48 else "WEAK_FIT"


def route(project: Path, task_file: Path, top: int=3, quiet: bool=False) -> Dict[str, Any]:
    task=load(task_file)
    errors=validate_task(task)
    if errors: raise SystemExit("\n".join(errors))
    cases=list_cases(project, successes_only=True)
    if not cases: raise SystemExit("没有可用的成功案例，请先 extract 或 add-case。")
    overall=sorted(((overall_score(c,task),c) for c in cases), key=lambda x:x[0], reverse=True)[:top]
    layer_leaders={}
    for layer in LAYERS:
        ranked=sorted(((layer_score(c,task,layer),c) for c in cases),key=lambda x:x[0],reverse=True)[:min(2,top)]
        layer_leaders[layer]=[{"id":c['id'],"title":c['title'],"score":s,"slice":c['slices'][layer]} for s,c in ranked]
    best=overall[0][0]
    result={
        "task_id":task["id"],
        "fit":fit_label(best),
        "overall_leaders":[{"id":c['id'],"title":c['title'],"score":s} for s,c in overall],
        "layer_leaders":layer_leaders,
        "difference_sheet":differences(overall[0][1],task),
        "note":"四层领航可以来自不同案例；不把局部观察升级为全局结论。"
    }
    dump(project / "outputs" / f"{task['id']}-route.json", result)
    if not quiet: print(json.dumps(result,ensure_ascii=False,indent=2))
    return result


def render_slice(layer: str, data: Dict[str,Any]) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(',',':'))


def compile_prompt(project: Path, task_file: Path, out: Path, top: int=3) -> None:
    task=load(task_file); routed=route(project,task_file,top,quiet=True)
    lines=[
        "# 案例罗盘 1.1｜四层迁移运行单","",
        "## 当前任务",task.get('input',''),"",f"覆盖度：{routed['fit']}","",
        "## 四层局部先例","",
        "只迁移可观察到的局部特征；不得复制原句，不得假装复原某个人。"
    ]
    for layer in LAYERS:
        lines += ["",f"### {layer}"]
        for item in routed['layer_leaders'][layer]:
            lines.append(f"- {item['id']}｜{item['title']}｜接近度 {item['score']:.3f}｜{render_slice(layer,item['slice'])}")
    lines += ["","## 差异迁移单"]
    for k in ["KEEP","REPLACE","ADD","REMOVE","WATCH"]:
        vals=routed['difference_sheet'][k]
        lines.append(f"- {k}: "+("；".join(map(str,vals)) if vals else "无"))
    lines += [
        "","## 生成顺序",
        "1. 先用 structure 先例确定信息顺序和转折位置。",
        "2. 再用 interaction 先例安排谁推动、谁反应、关系如何变化。",
        "3. 用 dialogue 先例控制轮次、问答、打断和潜台词密度。",
        "4. 最后用 voice 先例调整句长、停顿、标点和整体节奏。",
        "5. 全部人物、事实、题材、比喻和具体措辞按当前任务重新写。",
        "6. 输出完成品后，自检是否只继承了局部特征而没有拼贴来源。",
        "","## 当前硬要求",
        "必须包含："+"；".join(map(str,task.get('must_include',[]))),
        "必须避免："+"；".join(map(str,task.get('must_avoid',[]))),
        "","## 输出","只输出可直接使用的成品。"
    ]
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text("\n".join(lines)+"\n",encoding='utf-8')
    print(f"四层运行单已生成：{out}")


def metric_close(a: float,b: float, floor: float=.001) -> float:
    a=float(a or 0); b=float(b or 0)
    if a==0 and b==0: return 1.0
    return max(0.0,1.0-abs(a-b)/max(abs(a),abs(b),floor))


def load_source_text(project: Path, case: Dict[str,Any]) -> str:
    p=Path(str(case.get('source',{}).get('path','')))
    candidates=[p, project/p, project/'sources'/p.name]
    for x in candidates:
        if x.exists() and x.is_file():
            try: return x.read_text(encoding='utf-8')
            except Exception: pass
    return ''


def shared_run_length(output: str, sources: List[str], min_len: int=12, max_len: int=40) -> int:
    o=clean_text(output)
    if len(o)<min_len: return 0
    for n in range(min(max_len,len(o)),min_len-1,-1):
        grams={o[i:i+n] for i in range(len(o)-n+1)}
        for src in sources:
            s=clean_text(src)
            if any(s[i:i+n] in grams for i in range(max(0,len(s)-n+1))): return n
    return 0


def audit_output(project: Path, task_file: Path, output_file: Path, out: Path|None=None) -> Dict[str,Any]:
    task=load(task_file); text=output_file.read_text(encoding='utf-8')
    routed=route(project,task_file,top=3,quiet=True); fp=text_fingerprint(text)
    by_id={c['id']:c for c in list_cases(project,successes_only=True)}
    voice_case=by_id[routed['layer_leaders']['voice'][0]['id']]
    dia_case=by_id[routed['layer_leaders']['dialogue'][0]['id']]
    struct_case=by_id[routed['layer_leaders']['structure'][0]['id']]
    vf=voice_case['fingerprint']; df=dia_case['fingerprint']; sf=struct_case['fingerprint']
    voice_sim=mean([metric_close(fp.get(k),vf.get(k)) for k in ['avg_sentence_chars','sentence_length_cv','question_rate','exclaim_rate','ellipsis_rate']])
    dialogue_sim=mean([metric_close(fp.get(k),df.get(k)) for k in ['dialogue_turn_count','avg_dialogue_turn_chars','speaker_alternation']])
    structure_sim=mean([metric_close(fp.get('paragraph_count'),sf.get('paragraph_count')),length_fit(fp.get('char_count'),task['coordinates'].get('length'))])
    must_in=task.get('must_include',[]); must_out=task.get('must_avoid',[])
    include_hits=sum(1 for x in must_in if str(x) in text); avoid_hits=sum(1 for x in must_out if str(x) in text)
    requirement_score=((include_hits/max(1,len(must_in))) if must_in else 1.0)*.6 + ((1-avoid_hits/max(1,len(must_out))) if must_out else 1.0)*.4
    sources=[load_source_text(project,c) for c in by_id.values()]
    overlap=shared_run_length(text,[s for s in sources if s])
    originality=1.0 if overlap<12 else .75 if overlap<16 else .35 if overlap<24 else 0.0
    mechanical=round4(2.4*voice_sim+1.6*dialogue_sim+1.8*structure_sim+2.2*requirement_score+2.0*originality)
    result={
        'task_id':task['id'],'mechanical_score_10':mechanical,
        'voice_similarity':round4(voice_sim),'dialogue_similarity':round4(dialogue_sim),'structure_similarity':round4(structure_sim),
        'requirement_proxy':round4(requirement_score),'longest_shared_run':overlap,'originality_proxy':round4(originality),
        'output_fingerprint':fp,
        'verdict':'PASS' if mechanical>=8 and originality>.3 else 'REVIEW',
        'warning':'这是机械验收，不替代对剧情逻辑、人物真实性和语义质量的人工/模型复核。'
    }
    target=out or project/'audits'/f"{task['id']}-audit.json"; dump(target,result)
    print(json.dumps(result,ensure_ascii=False,indent=2)); return result


def validate_project(project: Path) -> int:
    errors=[]
    if not (project/'project.json').exists(): errors.append('缺少 project.json')
    ids=set()
    for c in list_cases(project):
        errors += validate_case(c)
        if c.get('id') in ids: errors.append(f"案例 ID 重复：{c.get('id')}")
        ids.add(c.get('id'))
    if errors:
        print('VALIDATION FAILED')
        for e in errors: print('-',e)
        return 1
    print(f"VALIDATION PASS｜案例数：{len(ids)}｜四层字段：PASS")
    return 0


def record_result(project: Path, result_file: Path) -> None:
    data=load(result_file)
    if 'task_id' not in data or 'accepted' not in data: raise SystemExit('结果卡至少需要 task_id 和 accepted')
    dump(project/'results'/f"{data['task_id']}.json",data)
    for cid in data.get('leader_ids',[]):
        p=project/'cases'/f'{cid}.json'
        if p.exists():
            c=load(p); stats=c.setdefault('local_usage',{'used':0,'accepted':0,'rejected':0})
            stats['used']+=1; stats['accepted' if data['accepted'] else 'rejected']+=1; dump(p,c)
    print(f"结果已回写：{data['task_id']}")


def main() -> int:
    p=argparse.ArgumentParser(description='案例罗盘蒸馏 1.1 CLI')
    sp=p.add_subparsers(dest='cmd',required=True)
    sp.add_parser('guide')
    x=sp.add_parser('init'); x.add_argument('project'); x.add_argument('--name',default='我的案例罗盘')
    x=sp.add_parser('extract'); x.add_argument('project'); x.add_argument('source_file'); x.add_argument('--id',required=True); x.add_argument('--title',required=True); x.add_argument('--status',default='success',choices=['success','failure','draft']); x.add_argument('--domain',default='writing'); x.add_argument('--job',default='general'); x.add_argument('--format',default='text'); x.add_argument('--audience',default='general'); x.add_argument('--tone',default=''); x.add_argument('--constraints',default=''); x.add_argument('--starting-state',default=''); x.add_argument('--ending-state',default=''); x.add_argument('--why-successful',default=''); x.add_argument('--proof-type',default='user_approved'); x.add_argument('--score',type=float,default=8.0)
    x=sp.add_parser('add-case'); x.add_argument('project'); x.add_argument('case_file')
    x=sp.add_parser('build-map'); x.add_argument('project')
    x=sp.add_parser('route'); x.add_argument('project'); x.add_argument('task_file'); x.add_argument('--top',type=int,default=3)
    x=sp.add_parser('compile'); x.add_argument('project'); x.add_argument('task_file'); x.add_argument('--out',required=True); x.add_argument('--top',type=int,default=3)
    x=sp.add_parser('audit'); x.add_argument('project'); x.add_argument('task_file'); x.add_argument('output_file'); x.add_argument('--out')
    x=sp.add_parser('validate'); x.add_argument('project')
    x=sp.add_parser('record'); x.add_argument('project'); x.add_argument('result_file')
    a=p.parse_args()
    if a.cmd=='guide': print(GUIDE)
    elif a.cmd=='init': init_project(Path(a.project),a.name)
    elif a.cmd=='extract': extract_case(Path(a.project),Path(a.source_file),a)
    elif a.cmd=='add-case': add_case(Path(a.project),Path(a.case_file))
    elif a.cmd=='build-map': build_map(Path(a.project))
    elif a.cmd=='route': route(Path(a.project),Path(a.task_file),a.top)
    elif a.cmd=='compile': compile_prompt(Path(a.project),Path(a.task_file),Path(a.out),a.top)
    elif a.cmd=='audit': audit_output(Path(a.project),Path(a.task_file),Path(a.output_file),Path(a.out) if a.out else None)
    elif a.cmd=='validate': return validate_project(Path(a.project))
    elif a.cmd=='record': record_result(Path(a.project),Path(a.result_file))
    return 0

if __name__=='__main__': raise SystemExit(main())
