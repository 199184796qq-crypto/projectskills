# 逼真度与镜头语言层

## 一、蒸馏目标

把电影级AI画面的“像真的”拆成可执行规则：人物、场景、道具的材质与物理证据，光影的方向与层次，运镜的目的，切镜的承接，镜头语言的叙事功能。

公开资料显示，参考项目的关键不是一次生成成功，而是大量生成、严格筛选、资产一致性工具、长提示词、自然光和物理约束共同工作。使用本层时，不复制原作角色或镜头，只复用这套质量控制逻辑。

## 二、人物逼真度

人物要像电影剧照，不像概念图。每个主角提示词至少锁定：

```text
年龄/体型 + 面部锚点 + 发型状态 + 皮肤质感 + 服装材质 + 伤口/汗/灰尘 + 眼神目标 + 身体重量 + 当前动作
```

优先写可见细节：

- 皮肤：汗、油光、毛孔、擦伤、血迹、灰尘，不要“完美磨皮”。
- 头发：湿发贴额、散乱发丝、逆光边缘，不要整齐塑料头发。
- 眼神：看向具体对象或威胁，不写“深邃有戏”。
- 表演：目标驱动的紧绷、迟疑、压制、反应，不写单纯情绪标签。
- 身体：脚步打滑、肩膀后缩、手指用力、呼吸急促，让动作有重量。

人物负面约束：

```text
no face drift, no waxy skin, no beauty retouch, no mismatched eyes, no dead stare, no duplicated face, no extra limbs, no changed hairstyle, no changed costume, no floating body, no exaggerated grimace
```

## 三、场景逼真度

场景要有“可进入的空间”，不是背景贴片。每个场景提示词至少锁定：

```text
地理/时代质感 + 空间结构 + 前中后景 + 主光源 + 可互动物件 + 地面/墙面材质 + 空气介质 + 危险源
```

优先写：

- 空间纵深：门、巷口、楼梯、通道、柱子、墙角、远处光源。
- 材质磨损：剥落墙皮、湿地反光、金属锈蚀、裂纹、灰尘。
- 空气介质：烟、雾、热浪、雨丝、尘埃、火花。
- 可互动元素：招牌、桌椅、电线、布帘、碎石、玻璃、水坑。
- 世界规则痕迹：符纹、裂缝、反常重力、影子变形、能量烧痕。

场景负面约束：

```text
no empty generic background, no plastic surfaces, no flat stage lighting, no random neon, no inconsistent era props, no impossible architecture unless marked as supernatural, no clean showroom texture
```

## 四、道具逼真度

道具必须有重量和状态变化。每个关键道具提示词至少锁定：

```text
尺寸 + 材质 + 磨损 + 重量感 + 持有方式 + 反光/污渍 + 当前状态 + 上一镜状态 + 下一镜状态
```

优先写：

- 手如何握：指节压白、掌心出血、指尖沾灰。
- 材质如何反光：铜锈暗光、玻璃碎反射、湿木吸光、金属冷光。
- 破损如何延续：裂纹位置、缺口方向、烧焦痕迹。
- 特效如何作用：发光、震动、发热、渗血、褪锈、开裂。

道具负面约束：

```text
no prop swap, no wrong hand, no disappearing object, no size change, no clean new surface if previously damaged, no unreadable magic symbol, no floating prop
```

## 五、光影效果

先写光源，再写氛围。

### 主规则

```text
light source -> direction -> quality -> color temperature -> shadow behavior -> reflective surfaces -> continuity
```

电影级AI画面常用：

- 自然低照度：主光来自门缝、窗、天井、火光、屏幕、雷光。
- 侧逆光：人物脸部半边在阴影里，边缘有轮廓光。
- 阴影侧拍摄：镜头在暗侧看人物，让高光从背后或侧后方切出轮廓。
- 局部高光：汗水、血迹、金属、眼睛、玻璃承担亮点。
- 低饱和基底 + 有限高纯色能量光：避免全画面彩色发光。

光影提示词模板：

```text
Natural low-key lighting, the key light comes from [direction/source], the camera stays on the shadow side of the face, [secondary color] rim light outlines the shoulders, wet surfaces catch small highlights, deep background remains readable, no flat front light.
```

光影负面约束：

```text
no flat front lighting, no overlit AI sheen, no random glow, no blown highlights on the face, no directionless light, no sudden color temperature shift between shots
```

## 六、运镜手法

运镜必须服务一种功能：

| 功能 | 运镜 |
| --- | --- |
| 建立空间 | 慢推、稳定横移、广角跟随 |
| 压迫角色 | 低机位逼近、窄空间手持、长焦压缩 |
| 进入主观恐慌 | 贴身手持、轻微失焦、呼吸感晃动 |
| 展示动作清晰度 | 中景/全景保持轴线，少切 |
| 展示奇观 | 环绕、升格、拉远、从物理反馈到主体 |
| 情绪落点 | 缓慢推近眼睛、手、道具或伤口 |

运镜提示词模板：

```text
The camera starts on [specific detail], then [movement type] toward [subject], staying on [camera side], keeping [landmark] in the background, ending on [emotion/action/detail].
```

运镜负面约束：

```text
no random camera drift, no sudden orbit without motivation, no axis flip, no subject leaving frame, no floating camera through solid objects
```

## 七、切镜手法

每个切镜必须有承接理由。

常用切镜：

- 动作匹配：手落下切到道具震动。
- 视线匹配：角色看向门口，切到门口敌人。
- 声音桥：雷声、枪声、呼吸、碗筷声延续到下一镜。
- 道具桥：铜钱、符纸、血滴、裂纹成为切点。
- 情绪桥：角色压住泪，切到导致他压抑的对象。
- 反差切：日常热闹切到灾变冷寂，但要有声音或道具相连。
- 集尾钩子切：当前危险结果切到远处同频预警。

切镜模板：

```text
Cut on [action/sound/gaze/prop]. The next shot begins with the same [motion/sound/object direction], preserving screen direction and emotional pressure.
```

## 八、镜头连贯性

每镜必须锁定：

```text
人物：位置、朝向、表情、服装、伤口、血迹。
道具：在哪只手、是否破损、是否发光、是否沾血。
空间：敌我方向、入口出口、地标位置、运动轴线。
光线：主光方向、色温、强弱、是否闪烁。
动作：上一镜结束动作，下一镜起始动作。
```

多镜头连续提示词：

```text
Continuity locks: [character] remains [position/orientation], [prop] stays in [hand/location], [wound/damage] remains visible, the key light continues from [direction], screen direction is preserved from left to right.
```

## 九、镜头语言质量评分

每项0-2分，总分20分：

| 维度 | 2分标准 |
| --- | --- |
| 人物逼真度 | 皮肤、眼神、服装、身体重量都有证据 |
| 场景逼真度 | 空间可进入，材质和空气介质可信 |
| 道具逼真度 | 材质、比例、握持、状态变化清楚 |
| 光影方向 | 光源、阴影、高光和反射明确 |
| 运镜动机 | 每次运动都有叙事功能 |
| 切镜承接 | 切点有动作/视线/声音/道具/情绪桥 |
| 连续性 | 人物、道具、光线、轴线不漂移 |
| 动作清晰度 | 危险、反应、后果可读 |
| 奇观物理性 | 特效改变环境和身体 |
| AI瑕疵控制 | 有针对性负面约束和淘汰标准 |

16分以下不进入最终成片，先返工提示词或资产锁定。
