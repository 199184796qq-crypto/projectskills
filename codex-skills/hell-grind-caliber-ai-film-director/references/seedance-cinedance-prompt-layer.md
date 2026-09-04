# Seedance/Higgsfield视频提示词层

## 核心原则

最终视频提示词要清楚、具体、可生成。优先使用简单直接的电影英文，少用抽象诗意形容。每条提示词只写当前镜头中可见、可听、必须出现的内容。

## 四步方法

### 1. Deconstruct

只提取当前镜头：

- 活跃角色、地点、道具、怪物、车辆、特效
- 当前动作、对白、时长、画幅
- 第一帧可见内容
- 角色站位、视线、身体朝向、移动路径
- 光线方向、声音需求、禁止带入的前文

删除无关角色、旧场景残留、上一镜提示词、剧本场号、不可见设定。

### 2. Diagnose

写提示词前检查风险：

- 第一帧是否可能空？
- 主体是否出现太晚？
- 角色是否离关键地标太远？
- 左右站位是否会翻转？
- 视线和身体朝向是否含糊？
- 镜头会不会选错侧位？
- 道具会不会跑到错误的手？
- 动作是否会变漂浮？
- 对白是否会错时？
- 多镜头切换是否会重置连续性？

有风险就加入短而硬的锁定句。

### 3. Develop

按以下顺序构建视频提示词：

```text
Scene Context
Output Settings
Active References
First Frame
Spatial Blocking
Camera and Lens
Character Performance
Action Timing
Lighting
Dialogue/Audio
Continuity Locks
Negative Constraints
Quality Suffix
```

### 4. Deliver

如果用户要直接生成，最终给英文提示词。中文说明只保留必要制作提示，不要把分析塞进最终提示词。

## 关键锁

### 第一帧锁

第一帧必须有主体、动作和空间关系：

```text
The first frame already shows [subject] in [exact position], [doing visible action], with [landmark] [distance/direction].
```

### 空间调度锁

```text
[Character A] stays on screen left, facing screen right. [Character B] stands three steps away on screen right, facing A. The camera remains on the same side of the action line.
```

### 视线与身体朝向

明确写：

- looking at
- turning toward
- body angled away from
- shoulders facing
- back to camera

### 镜头焦段

按任务选择：

- 标准视角：关系、对白、普通调度。
- 广角：空间压迫、近距离动作、夸张透视。
- 短长焦：人像、表演、背景压缩。
- 长焦：远距离观察、压迫、孤立角色。

不要只写“cinematic lens”，要写可见结果。

### 物理锁

动作必须有重量、接触和反作用：

```text
His boots slip on the wet floor before he regains balance.
The impact pushes her shoulder back and scatters dust from the wall.
```

### 光线锁

写光从哪里来：

```text
Cold blue light comes from the broken window on camera left; warm firelight flickers from below, never changing direction.
```

## Seedance成片提示词模板

```text
Scene Context:
[one concise sentence]

Output Settings:
[duration, aspect ratio if needed, single continuous shot or cuts]

Active References:
[only references visible in this exact shot]

First Frame:
[subject already visible, exact position, action, landmark]

Spatial Blocking:
[left/right, distance, gaze line, body orientation, action line]

Camera and Lens:
[shot size, lens behavior, camera side, movement path]

Character Performance:
[objective, obstacle, tactic, visible beat change]

Action Timing:
[0-2s / 2-4s / 4-6s if useful]

Lighting:
[direction, color, continuity]

Dialogue/Audio:
[only if needed, exact timing]

Continuity Locks:
[costume, prop hand, wounds, location, light]

Negative Constraints:
[no extra characters, no duplicated bodies, no prop swap, no gaze flip, no empty opening]

Quality Suffix:
cinematic, physically grounded motion, stable identity, clear readable action, no prompt pollution
```

## 自检

- 当前镜头有没有无关角色或旧tag？
- 第一帧是否已经有主体？
- 道具在哪只手？
- 人物左右是否锁定？
- 机位是否在同一轴线侧？
- 光线方向是否稳定？
- 动作是否有物理反馈？
- 对白是否在正确时点发生？
