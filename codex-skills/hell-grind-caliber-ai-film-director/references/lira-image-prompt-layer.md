# Lira图像提示词层

## 核心原则

图像提示词要服务资产稳定，不是堆关键词。先判断目标模型和任务，再写自然、短而清楚的英文提示词。平台参数如画幅、分辨率、种子、按钮设置不要混进正文。

## 四步方法

```text
Deconstruct -> Diagnose -> Develop -> Deliver
```

### Deconstruct

识别：

- 任务类型：角色、场景、道具、关键帧、修图、纹理清理。
- 目标模型：Soul 2.0、Soul Cinema、Cinema Studio AI Cast、NBP、Seedream 4.5、GPT Image 2或其他。
- 已给信息与缺失信息。

### Diagnose

检查：

- 主体数量是否过多。
- 摄影机角度、光线、构图是否含糊。
- 角色一致性是否只靠文字硬撑。
- 是否有文字、纹身、复杂标志等高失败元素。
- 是否提示词过长、关键词堆叠。
- 修图是否会误伤原图。

### Develop

按任务选路线：

- 角色：身份锚点、年龄体型、发型脸部、服装、道具、三视图或参考表。
- 场景：镜头位置、空间结构、光线方向、色彩、材质、时代质感。
- 道具：材质、比例、形态、磨损、干净背景。
- 修图：最小CHANGE，详尽PRESERVE EXACTLY。
- 纹理清理：只修皮肤、布料、墙面、金属等表面质感，不改构图和主体。

### Deliver

输出用户语言说明，提示词正文优先用英文。需要多个模型时，分模型给不同提示词。

## 模型路由

| 任务 | 优先路线 |
| --- | --- |
| 角色一致性/角色表 | Soul 2.0 或 Cinema Studio AI Cast |
| 场景/电影关键帧 | Soul Cinema |
| 道具图/产品式资产 | NBP 或 GPT Image 2 |
| 已有画面局部修改 | NBP优先 |
| 成片纹理脏、皮肤布料金属不干净 | Seedream 4.5纹理清理 |
| 极小范围局部手术或反打视角 | GPT Image 2兜底 |

## 反失败规则

- 用自然语言，不要关键词堆叠。
- 正向描述优先，负面约束只写关键风险。
- 不要把平台参数写进提示词正文。
- 写技术光线和材质，不写空泛氛围。
- 控制调色板，避免一锅乱色。
- 角色一致性靠锚点和参考ID，不靠长篇形容。
- 写实图要防插画漂移。
- 修图不要重建整张图，只写改变和保留。

## 图像提示词模板

### 角色资产

```text
A cinematic character reference sheet of [character], [age/body], [face and hair anchors], wearing [locked costume], holding/wearing [signature prop], [3-panel front/side/three-quarter view if needed], neutral background, consistent identity, realistic skin and fabric detail, controlled lighting.
```

### 场景/关键帧

```text
A cinematic still of [location], [spatial layout], [main subject if any], [camera angle and shot size], [light direction], [palette], [materials and atmosphere], high-budget film frame, grounded realism.
```

### 道具

```text
A clean prop design image of [prop], [shape], [material], [scale clue], [surface details], centered product-style framing, neutral background, no readable text unless explicitly required.
```

### NBP修图

```text
CHANGE: [only the exact local change].
PRESERVE EXACTLY: subject identity, pose, camera angle, lighting direction, background layout, clothing, hands, facial expression, color palette, all untouched objects.
```

## 自检

- 是否选对模型路线？
- 是否主体清晰且数量可控？
- 是否锁住身份、服装、道具？
- 光线和构图是否明确？
- 是否避免不必要文字和标志？
- 修图是否只改该改的地方？
