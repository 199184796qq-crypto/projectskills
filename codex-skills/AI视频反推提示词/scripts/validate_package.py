#!/usr/bin/env python3
from pathlib import Path
import json, hashlib, sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "SKILL.md","README.md","QUICKSTART.md","PACKAGING.md",
    "templates/quick-reverse.md","templates/full-reverse.md",
    "templates/multi-shot.md","templates/compare-repair.md",
    "evals/evals.json","PACKAGE-MANIFEST.json","SHA256SUMS.txt"
]
errors = []
for rel in required:
    if not (ROOT / rel).exists():
        errors.append(f"missing: {rel}")

try:
    evals = json.loads((ROOT / "evals/evals.json").read_text(encoding="utf-8"))
    if len(evals.get("cases", [])) < 10:
        errors.append("eval cases fewer than 10")
except Exception as e:
    errors.append(f"evals invalid: {e}")

try:
    manifest = json.loads((ROOT / "PACKAGE-MANIFEST.json").read_text(encoding="utf-8"))
    for item in manifest["files"]:
        p = ROOT / item["path"]
        if not p.exists():
            errors.append(f"manifest missing file: {item['path']}")
            continue
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if h != item["sha256"]:
            errors.append(f"hash mismatch: {item['path']}")
except Exception as e:
    errors.append(f"manifest invalid: {e}")

skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
for phrase in ["关键状态","过渡桥","下一镜起点","最早偏差时间码","稳定性限制"]:
    if phrase not in skill:
        errors.append(f"core method missing: {phrase}")

if errors:
    print("FAIL")
    for e in errors:
        print("-", e)
    sys.exit(1)
print("PASS: package structure, core method, evals, templates, and manifest hashes validated")
