---
name: case-compass-distiller
description: 将少量授权案例做成四层局部先例地图。新任务到来时，分别寻找结构、声音、对白和互动上的近例，通过差异迁移完成新作品，并用反向验收检查硬要求和原句重叠。
license: MIT
---

# 案例罗盘蒸馏 Skill 1.1

## 一句话定位

**放进几个你认可的案例，我把它们拆成四种局部先例；新任务来了，分别找最接近的结构、声音、对白和人物互动，再按差异重新创作。**

这不是人格复原，也不是通用方法总结。每个观察只在原案例附近有效，系统不把少量案例升级成永远正确的结论。

## 上来就用：六问引导

用户没有准备结构化材料时，按顺序询问并立即执行：

1. 想让它学会完成什么具体任务？
2. 请给 3—12 个用户有权使用、并且认可的案例。
3. 哪些案例最成功，成功依据是什么？不知道可写“用户认可”。
4. 新任务主要需要继承什么：结构、语气、对白还是人物互动？可多选。
5. 有哪些硬要求、禁区、长度和受众？
6. 现在用哪个新任务立即测试？

材料到齐后，不写长篇理论，直接执行：**自动建卡 → 四层建图 → 分层找近例 → 差异迁移 → 输出成品 → 反向验收。**

## 四层局部先例

### 结构切片
只记录信息顺序、段落槽位、转折位置、节奏分布和收束方式。它回答“内容怎么推进”，不携带原案例的具体故事。

### 声音切片
只记录可观察语言现象：句长区间、长短句变化、疑问与感叹密度、停顿方式、直白或含蓄程度。它不使用“像某某本人”作为证据。

### 对白切片
记录对话轮次、单轮长度、问答关系、打断、沉默、潜台词浓度和信息藏露方式。不同角色的对白必须分开观察，禁止把所有人物写成同一张嘴。

### 互动切片
记录谁先推动、谁后反应、权力怎样移动、冲突如何升级、动作与台词如何接力。它用于迁移场景动力，不推测人物的真实人格。

四层可以分别选择不同领航案例。例如，结构参考案例A，语言节奏参考案例B，对白参考案例C，人物互动参考案例D。这样不必强迫一个案例包办全部能力。

## 自动建卡

拿到授权原文后，先提取机器可测特征，再由模型补充语义观察：

1. 计算句长、段落、标点、对话轮次、说话人数量和轮换程度；
2. 划分结构、声音、对白、互动四层；
3. 每层只写“原文中可直接观察到什么”；
4. 对不确定内容写 `unknown` 或“需要复核”；
5. 不保存长句摘要，不把罕见比喻和独特措辞写进运行卡；
6. 登记来源授权与哈希，用于重复检查和原句安全审计。

CLI 可直接执行：

```bash
python tools/compass.py init my_project --name "编剧案例罗盘"
python tools/compass.py extract my_project sample.txt --id case-001 --title "样例一" --job screenplay --format script --tone "克制,冷幽默"
python tools/compass.py build-map my_project
```

## 新任务运行

新任务到来时，必须依次完成：

1. 为四层分别寻找 1—2 个近例；
2. 输出 `KEEP / REPLACE / ADD / REMOVE / WATCH` 差异单；
3. 先迁移结构，再迁移互动，再处理对白，最后校准声音；
4. 所有人物、事件、题材、事实、比喻和具体句子全部按新任务重写；
5. 没有接近案例时降级为试作，不宣称已经学会；
6. 完成后反向检查：继承了哪些局部特征、遗漏了哪些硬要求、有没有来源原句拼贴。

```bash
python tools/compass.py route my_project task.json --top 3
python tools/compass.py compile my_project task.json --out runtime_prompt.md
```

把 `runtime_prompt.md` 交给当前模型执行即可。它已经包含四层领航和迁移顺序。

## 编剧、剧本与说话方式怎么蒸

针对编剧或剧本，至少放入 5 个案例，最好覆盖不同场景。系统分别观察：

- 剧情怎样进入场景、怎样制造变化、怎样退出；
- 角色说话是长句还是短句，是先结论还是先铺垫；
- 冲突时角色如何回避、逼问、打断、反击或沉默；
- 信息是直接说出，还是通过动作、误解和反应暴露；
- 不同人物之间是否存在稳定的声音距离。

只提供成品剧本时，可以蒸出可观察的创作模式和语言表现；材料越同质，迁移越稳定。想跨题材仍保持效果，应提供不同题材但同一种创作手感的案例。

## 已验证的叙述样式

当用户要求创作“第一人称闯关式探店、体验或县城日常 Vlog 旁白”时，读取 [references/first-person-task-narration.md](references/first-person-task-narration.md)。只迁移任务推进、现场反应和幽默机制；不得复制来源人物、原句、具体身份设定或引导欺骗、白嫖、虚假承诺的做法。


## 反向验收

成品生成后运行：

```bash
python tools/compass.py audit my_project task.json output.txt
```

工具会检查：

- 句长、节奏和标点与声音先例的接近程度；
- 对话轮次和说话人轮换是否接近对白先例；
- 长度、段落和基本结构是否匹配；
- 硬要求的机械命中情况；
- 与来源是否出现过长连续重叠。

机械分达到 8 分只能说明“形式与硬约束基本合格”，剧情逻辑、人物真实性和艺术质量仍需模型或人工复核。

## 八分使用条件

达到稳定约 8/10，建议满足：

- 至少 5 个质量可靠、来源授权的案例；
- 案例之间既有共同手感，又有一定场景差异；
- 四层观察至少人工复核一次；
- 新任务与案例库不是完全陌生领域；
- 输出后执行反向验收，并根据失败结果补充案例。

只有 1—2 个案例，或要求跨越完全陌生题材时，只能交付试作。

## 硬边界

- 不根据姓名、名气、身份标签或公众印象生成写法；
- 不复制来源中的独特长句、连续措辞或罕见比喻；
- 不把局部案例宣布为普遍方法；
- 不把不同角色的语言混成统一腔调；
- 不把机械验收分伪装成真实创作质量分；
- 不在证据不足时补写所谓深层动机；
- 不把失败案例作为正向领航，但保留其危险信号；
- 不引入其他蒸馏系统的专有架构、术语或流程。

## 完整命令

```bash
python tools/compass.py guide
python tools/compass.py init PROJECT
python tools/compass.py extract PROJECT SOURCE --id ID --title TITLE
python tools/compass.py add-case PROJECT CASE.json
python tools/compass.py build-map PROJECT
python tools/compass.py route PROJECT TASK.json --top 3
python tools/compass.py compile PROJECT TASK.json --out runtime_prompt.md
python tools/compass.py audit PROJECT TASK.json output.txt
python tools/compass.py record PROJECT result.json
python tools/compass.py validate PROJECT
python tools/run_selfcheck.py
```
