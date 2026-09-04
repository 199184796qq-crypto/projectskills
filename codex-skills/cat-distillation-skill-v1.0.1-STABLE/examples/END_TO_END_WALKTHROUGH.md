# 端到端样例：虚构创作者“林小岚”

本样例完全虚构，不对应真实人物。

1. `corpus/` 中放入四份短材料：小说场景、剧本片段、专栏片段、一次改稿对话；
2. `sources.jsonl` 登记来源；
3. 从材料中提出五条爪印候选；
4. 经过强弱样本对照，三条进入 active，一条保留 tested，一条降为 hypothesis；
5. 使用 `compile` 生成小说和剧本运行包；
6. 使用 `leak-check` 检查一份新稿；
7. 用户纠正进入 `feedback.jsonl`。

命令：

```bash
python tools/catdistill.py validate --project examples/fictional_creator
python tools/catdistill.py nutrition --project examples/fictional_creator
python tools/catdistill.py compile --project examples/fictional_creator --mode MAKE --recipe novel
python tools/catdistill.py compile --project examples/fictional_creator --mode MAKE --recipe screenplay
python tools/catdistill.py leak-check --project examples/fictional_creator --text examples/fictional_creator/compiled/safe_sample.txt
```
