# 五分钟开始

1. 运行 `python tools/compass.py init my_project`。
2. 把 3—12 个有权使用的案例原文放进项目。
3. 每个案例运行一次 `extract`，自动生成四层先例卡。
4. 检查卡片中的 `manual_notes`，必要时补充场景功能、潜台词和人物互动观察。
5. 填写 `templates/TASK.json`，运行 `route` 与 `compile`。
6. 让模型执行生成出的 `runtime_prompt.md`。
7. 把成品保存为文本，运行 `audit`。

最小示例：

```bash
python tools/compass.py init my_project --name "我的编剧罗盘"
python tools/compass.py extract my_project sources/a.txt --id a --title "场景A" --job screenplay --format script --tone "克制,紧张"
python tools/compass.py build-map my_project
python tools/compass.py compile my_project tasks/test.json --out outputs/run.md
python tools/compass.py audit my_project tasks/test.json outputs/final.txt
```

别先写理论报告。先建卡，立刻拿一个新任务测试。
