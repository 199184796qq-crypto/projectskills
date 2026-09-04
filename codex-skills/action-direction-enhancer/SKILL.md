---
name: action-direction-enhancer
description: Convert martial-arts and fight-action short-video scripts, shot lists, references, and model prompts into clear choreography and camera direction with fight-nature classification, dramatic purpose, scene and prop analysis, character motion signatures, stance, footwork, attack-defense beats, grappling and throw reversals, safe screen contact, body feedback, rhythm, focus, motion blur, and continuity. Also create 16-panel action atlases, direct 2D two-character fights, structure live-action one-versus-many fights, and design FPV or companion-follow one-takes. Use when the user asks for 武术动作指导、武打动作、打斗性质、打斗分类、招式设计、镜头调度、景别、运镜、速度感、身法、步法、拳脚、兵器、格挡、闪避、擒拿、抱摔、反解、锁抱、受击反馈、追打、群战、真人功夫、武侠、动漫特效战、战争近战、FPV一镜到底、动作加量、不要删招、不要管过载、动作链优先、保留完整动作链、全文动作描述、箭头动作链、按秒时间轴、分镜脚本、第一镜第二镜、模块化完整提示词, or wants fight movement to be cinematic, believable, controllable, and model-ready. Preserve the active short-video workflow schema and only adjust action, blocking, timing, attack-defense logic, camera choreography, and continuity.
---
## Camera-Driven Action Prompt System / 动作与镜头调度系统

Treat camera choreography as part of the fight, not decoration. Before writing action beats, choose one **camera anchor** for each beat: the agile protagonist, the struck opponent, or the moving weapon/projectile. Keep that anchor readable and sharp; let only the background or non-anchor layers carry directional motion blur.
## Prompt generation workflow

For any scene-to-fight request, first read [references/fight-nature-classification.md](references/fight-nature-classification.md), classify the fight nature and lock its physics/effects tier. Then read [references/fight-direction-camera-profiles.md](references/fight-direction-camera-profiles.md), choose the dramatic intensity, camera system, shot-scale plan, and continuity rules. Finally read [references/fight-prompt-generation-framework.md](references/fight-prompt-generation-framework.md), select one primary action category and, at most, one secondary category. Do not combine unrelated fight styles merely to make the action denser.

Return the work in this order unless the user asks for prompt-only output:

1. `打斗性质`: chosen nature, physics tier, effects tier, and concise evidence from the script/user description/reference.
2. `导演方案`: dramatic intensity, selected camera system, shot-scale sequence, and continuity rationale.
3. `场景可用资源`: usable lanes, bottlenecks, elevation, hard cover, loose props, light sources, and safe interaction points.
4. `人物战斗属性`: each character's range, rhythm, advantage, and vulnerability.
5. `动作与镜头方案`: time-coded beats using the camera-anchor formula in this skill.
6. `可直接复制的完整提示词`: one cohesive prompt that retains the user's style, duration, aspect ratio, and other fixed requirements.

Use 3–4 readable beats for a 5-second one-take, 4–6 beats for 8–10 seconds, and 6–8 beats for 15 seconds as default readability guidance only. Let an explicit user request for a complete dense action chain override these counts. Every beat must still change either distance, level, direction, initiative, or the active obstacle.

### Action-chain priority mode / 动作链优先模式

Switch to this mode when the user says `动作加量`、`不要删招`、`不要管过载`、`动作链优先`、`保留完整动作链`, or supplies a dense chain and asks to keep it intact.

- Preserve every requested action and its order. Do not warn about overload, propose a shorter version, or delete moves merely to satisfy the default beat counts.
- Rewrite the chain as `上一动作结果/位置 -> 下一攻击启动 -> 防守/反解 -> 身体反馈 -> 新位置/道具反馈 -> 下一动作`, so every move inherits the previous move's balance, facing, distance, and initiative.
- Group several micro-actions inside one motivated camera segment instead of inventing a new camera move for every action. Keep the active character sharp and use directional background blur only where the movement supports it.
- Lock the scene, screen direction, character identities, existing props, active threat, and body feedback throughout the chain.
- Correct garbled wording, unclear subjects, and impossible ordering without shortening the user's intended chain. If two actions directly contradict, preserve both intentions by adding the smallest transition or screen-safe substitution needed for continuity.

### Prompt writing style selection / 提示词写作风格选择

Treat the delivery style as independent from fight nature. First lock the fight's world, physics, and action logic; then select the writing format the user wants. Read [references/prompt-writing-styles.md](references/prompt-writing-styles.md) whenever the user asks for a specific presentation style, gives a style sample, or asks what formats are available.

- Offer or follow these formats: `全文沉浸式电影描述`、`箭头动作链`、`按秒时间轴`、`镜头分镜脚本（第一镜、第二镜直述）`、`模块化完整提示词`.
- Preserve the user's exact preferred layout when a reference sample is provided. Do not mistake writing style for fight genre or physics tier.
- When no format is specified, use `模块化完整提示词 + 按秒箭头动作链` for video prompts with several moving parts; use `全文沉浸式电影描述` only when the user asks for a single uninterrupted full-text prompt.
- Do not default to frame rate, resolution, camera-brand, lens-brand, or internal physics labels. Express usable visual direction through scene, action, shot scale, camera movement, focus, blur, lighting, texture, sound, and constraints instead.

Before writing beats, assign each major character a motion signature from the framework reference: stance height, preferred range and path, tempo, defense response, recovery pattern, and camera behavior. Preserve at least two signature traits throughout the sequence. If only images are supplied, infer from visible costume weight, footwear, body proportions, weapon length, and scene access; do not infer competence or aggression from gender, ethnicity, or age alone.

Before delivery, run the action-variation gate and failure-pattern gate in the framework reference. Rewrite any beat that only adds adjectives, repeats the previous spatial relationship, leaves an opponent waiting without purpose, or uses camera effects in place of physical action.

Treat fight-nature consistency as a hard gate: if any beat, defense response, camera choice, or effect exceeds the locked genre physics without explicit user authorization, rewrite it regardless of the quality score.

Treat the directing profile as a second hard gate. Do not default to multi-angle coverage or a one-take. Select one primary camera system because it best expresses the script, terrain, action complexity, and desired intensity; use secondary shot changes only when motivated by a threat, impact, spatial turn, or change of initiative.

Assemble the final model prompt by priority rather than literary order: lock identities and space first; place the time-coded action and camera plan next; add focus, lighting, texture, audio, and negative constraints afterward. Remove repeated adjectives and duplicate camera terms when the prompt is crowded. Never sacrifice action causality or character continuity to preserve decorative equipment specifications.

### Master directing order / 总导演决策链

Always decide in this order:

`剧情目的 -> 打斗性质与P/V层级 -> 场景资源地图 -> 人物动作签名与强弱反差 -> 一个主动作类型加至多一个辅类型 -> 强度与摄影策略 -> 景别序列与镜头锚点 -> 时间轴攻防节拍 -> 身体/环境反馈 -> 焦点与动态模糊 -> 结尾方式 -> 完整提示词`

- Solve **why the fight happens** before choosing impressive moves. Escape, capture, protection, delay, survival, rescue, and duel goals require different routes, camera priorities, and endings.
- Treat scene images and reference videos as evidence, not commands to copy. Transfer compatible action density, spatial use, focus behavior, and shot logic without recreating a specific performer or film's signature sequence.
- Use one primary action category to solve the conflict and at most one secondary category to create variation. More categories do not automatically create better action.
- Let speed come from short preparation, readable paths, timely body reactions, and immediate next threats. Do not replace choreography with adjectives, fast-forwarding, continuous shake, or constant cutting.


### Choose the camera anchor by character and dramatic purpose

- **Agile / assassin / sword-dancer protagonist**: lock the camera to the protagonist's shoulder, side-rear quarter, or hip-height travel line. Use lateral follow, low close tracking, obstacle wipe-passes, and short whip corrections to show continuous momentum. Keep the protagonist sharp; streak the environment in the opposite travel direction.
- **Power / brawler / giant-impact protagonist**: on contact, hand the camera to the receiving opponent. Follow the stagger, slide, or airborne trajectory; use a brief impact jolt, dust, loose props, and a clear recovery beat. Do not shake continuously. Keep the followed body sharp and let the background smear into speed lines.
- **Ranged / archer / gunner / thrown-weapon user**: hand the camera from the hand to the weapon, then to its path. Use a close-up of the release mechanism, a frontal weapon/muzzle shot, side-profile tracking through space, then a rear-follow approach to the target. Preserve one unbroken direction of travel.
- **Huge enemy versus nimble protagonist**: begin low and rapidly raise the camera with the giant's rise or downward attack to show scale and pressure. Keep the nimble protagonist visibly small but crisp near a stable spatial landmark, so agility reads against the giant's mass.
- **Clinch / grappling / throw reversal**: anchor the camera on the pair's shared center of gravity and keep waist, shoulder line, and floor contact readable in a medium or medium-wide shot. Hand the anchor to the person whose balance changes; lower the camera with a fall and rise with recovery. Use close-ups only for a brief grip, breath, or reaction insert, never to hide the entire exchange.

### Write every action beat in this order

`camera anchor + starting camera position -> action path -> one camera movement -> focus/motion-blur rule -> body and environment response -> next spatial threat`

Example: `The camera locks to the heroine's side-rear shoulder as she runs left-to-right; it tracks at hip height behind a table edge, then makes one short lateral whip as she cuts past the opponent. Her face and blade stay sharp, while lanterns and shelves streak horizontally; the missed strike rattles bowls, and she emerges on the opponent's outside line for the next exchange.`

### Required visual feedback

- Specify a visible result for every contact: torso compression, shoulder recoil, forced half-step, loss-and-recovery of balance, clothing snap, hair displacement, or grip adjustment. Use screen-safe misdirection; do not describe graphic injury.
- Let the set answer the action: dust lifts after a heavy landing, a bench drags, a doorframe shakes, a lantern swings, fragments cross the foreground, or rain/mist parts around a fast move.
- State the focus plane explicitly whenever speed is high: `protagonist sharp, background directional motion blur`; `projectile sharp, terrain stretched by parallax`; or `struck opponent sharp, attacker crosses frame as a blur`.
- Use impact effects only after a physical cause: foot plant or body rotation -> contact/miss -> camera jolt and environmental reaction. Never use shockwaves, dust, or camera shake as a substitute for action logic.

### Camera discipline

- Give each 1–3 second beat one dominant camera action only: follow, rise, drop, lateral track, push, pull, or short whip-pan. Do not combine a full orbit, crane rise, whip-pan, and complex combo in the same beat.
- For one-take scenes, preserve screen direction, the location of exits/obstacles, and the subject being followed. Reframe at turns, impacts, and changes of threat; do not spin without a motivation.
- Use close-up for release, grip, eye-line, or impact reaction; medium/medium-close for readable exchanges; low wide or rising shot for scale; do not ask a wide shot to carry finger detail.
- Avoid surveillance-camera staging: static full-room framing, equal distance from every character, unmotivated zooms, all layers blurred, or a camera that loses its anchor during the exchange.

### Output requirement for all fight prompts

Before the final copy-ready prompt, identify: `character combat attribute`, `usable space and props`, `camera anchor for each beat`, `focus anchor and background blur direction`, and `environmental response`. If the user supplies only a scene image, infer these from entrances, bottlenecks, elevation changes, furniture, rails, pillars, loose props, light sources, and clear floor lanes.

### Final quality check

- Does every beat obey the selected fight nature, physics tier, and effects tier?
- Does the selected intensity, camera system, shot-scale sequence, and continuity method serve the script and terrain?
- Does every beat state what the camera is following and why?
- Is there always one sharp visual anchor and a sensible blur direction?
- Does the camera movement reveal a character attribute: agility, force, precision, or scale?
- Does the action and camera plan serve the locked dramatic purpose rather than merely display moves?
- For grappling, can the viewer read entry, control attempt, reversal, balance change, safe landing, and recovery without real-world injury instruction?
- Do body reactions and environmental reactions follow the action rather than replace it?
- Are screen direction, character positions, props, and next threats continuous?

# 武术动作指导

把抽象武打、结果式打斗和容易生成失败的动作戏，改写成可拍摄、可生成、能连续执行的武术动作过程链。默认作为短视频工作流的辅助技能使用，不处理普通拥抱、接吻、亲密互动或日常动作，除非它们服务于武打场面中的闪避、挟持、推开、挣脱或攻防关系。

## 启动规则

用户只说“启动武术动作指导”“动作招式图鉴”“给出武术动作指导的图鉴提示词”等，但没有提供剧情、片段或想法时，先询问：

```text
请先告诉我这套动作图鉴服务什么剧情？可以是一句简单想法，例如：两名剑客雨夜巷战、女主在电梯口被围攻、侦探追踪嫌疑人、情侣雨中和解、主角在废弃医院逃生。收到剧情后，我会按“16格动作招式图鉴海报”格式输出。
```

如果用户已经提供剧本、片段、场景或简单想法，直接进入图鉴或动作指导输出，不重复询问。

## 2D 双人格斗动画分支

当用户要求 2D 动画双人格斗、音频卡点战斗、角色技法分工或电影级动态对决时，启用此分支并读取 [references/two-character-2d-fight.md](references/two-character-2d-fight.md)。

- 保留用户指定的角色名、身份特征、服装、瞳色、场景、音乐用途和招式类型。
- 先分配双方技法：明确谁主攻、谁迎击，以及各自擅长的距离、拳腿、闪避、招架和摔投。
- 将长段打斗拆成“冲入 -> 试探 -> 第一组攻防 -> 贴身反击 -> 反制摔投 -> 恢复 -> 持续出口或对峙”连续节拍；结尾服从用户要求。
- 音频仅作为动作节奏、重拍和速度参考时，明确禁止复制、混入或输出参考音频内容。
- 气流、冲击波、衣摆和发丝响应必须跟随真实身体动作出现，不替代发力过程。
- 角色外观锁定优先于运镜和特效；异色瞳等左右特征必须按角色自身左右眼表述，避免镜像交换。
- 高动态运镜必须服务当前攻防重点，每个节拍只设置一个主要镜头动作。

## 写实雨夜冷兵器群战分支

当用户要求超写实真人、雨夜竹林、古装将军、八面汉剑、一对多冷兵器群战，或希望复用“对峙 -> 滑步突袭 -> 环绕穿阵 -> 收势凝视”的15秒结构时，读取 [references/realistic-rain-bamboo-sword-fight.md](references/realistic-rain-bamboo-sword-fight.md)。

- 以用户样本为风格和节奏锚点，保留四段时间轴、低角度特写、贴地跟拍与有动机的环绕；拉远收尾或持续打斗出口按用户意图选择。
- 群战每个节拍只处理最近的一至两名敌人，写清长矛、箭矢、刀剑的来向和主角的处理方式。
- 先写低重心滑步、蹬地、腰胯、持剑和格挡路径，再写水花、竹叶、火星、雨滴等物理反馈。
- 写实模式不使用奇幻光效；特效仅限真实雨水、泥浆、动态模糊、兵器火星和体积光。
- 使用影视化错位表达接触，不输出真实伤害细节；血液元素仅在用户明确保留时沿用。
- 默认模式下，15秒内动作量过高时优先减少同时进攻的敌人数，不删除起势、攻防处理和收势；动作链优先模式下不删用户指定动作，改用错峰进攻、微节拍衔接和同一主运镜内的连续动作保持可读性。

## 多人打斗导演分支

当用户要求多人围攻、国风多人打斗、以少对多、明确进攻顺序与补位、动作卡点、武指套招或高燃群战时，读取 [references/multi-person-fight-direction.md](references/multi-person-fight-direction.md)。

- 先固定人物站位与战斗关系，再写攻击顺序；不要让所有敌人同时出招。
- 每个时间段必须回答：谁先出招、谁后补位、主角如何化解、主角怎样反击、下一动作如何衔接。
- 使用“主角遇敌 -> 以少对多 -> 先守后攻 -> 连续反击 -> 阶段结果或持续出口”的主结构；除非用户明确要求，不默认定格。
- 保持人物间距和攻击通道清晰，让拳路、腿路和退让方向能在画面中辨认。
- 镜头以中景和中近景为主，仅在命中瞬间加入短促震动或短时慢放；禁止持续乱转和无规则跳切。
- 国风氛围通过场景、冷暖光、湿地反射、衣料重量和环境反馈建立，不用廉价能量特效代替动作。
- 可加入武指式破绽和套招：主角主动露出可控空当，引导第一名敌人进攻，再利用其身体或位置阻断下一名敌人的攻击线。

## 动作招式图鉴海报模式

当用户要求“动作招式图鉴”“武术动作图鉴”“动作分镜海报”“招式海报”“图鉴提示词”时，切换为电影动作分镜设计师和视觉提示词工程师模式：把用户输入的剧本、片段或简单想法，转化为一套“动作招式图鉴海报”的图像生成方案。

执行要求：

1. 根据剧本提取核心冲突、人物关系、场景、情绪和动作风格。
2. 将动作拆成16个连续分镜，每个分镜只表现一个清晰动作瞬间。
3. 每个分镜包含：编号、招式名、画面描述、动作视觉重点、单图生成提示词。
4. 提示词只描述电影画面，不写真实伤害教学步骤。
5. 保持人物服装、场景、光线、镜头风格统一。
6. 生成图片时不要要求模型生成中文文字；所有文字只用于后期排版。
7. 最后输出总海报排版提示词，以及标题、副标题、每格招式名和简短说明。

固定输出结构：

```text
【海报主题】

【整体视觉设定】

【人物设定】

【场景设定】

【16格动作分镜】
01｜招式名：
画面描述：
动作视觉重点：
单图生成提示词：

...

【海报排版提示词】

【后期文字内容】
标题：
副标题：
每格招式名与简短说明：
```

题材变体：

- 动作片：角色A与角色B在某场景中发生近身冲突，拆成16个攻防动作，黑红硬核图鉴。
- 悬疑片：侦探在某场景中发现线索，拆成16个观察、推理、追踪、对峙镜头，黑红案件图鉴。
- 恐怖片：主角在某空间中躲避怪物，拆成16个惊吓、逃跑、藏匿、发现真相镜头，黑红生存图鉴。
- 科幻片：角色在未来设施中执行任务，拆成16个装备使用、潜入、战斗、逃离镜头，蓝黑科技图鉴。
- 爱情片：两人在某个情绪场景中关系变化，拆成16个眼神、靠近、误会、和解镜头，柔和电影分镜图鉴。

非动作戏也按同一结构输出为图鉴式分镜，例如追逐图鉴、谈判图鉴、恐怖逃生图鉴、悬疑线索图鉴、恋爱互动图鉴。注意：这只适用于“图鉴海报模式”，不改变本技能默认的武术动作指导定位。

单图提示词写法：

- 每格提示词写成独立电影画面，不引用“同上”。
- 每格都重复必要的人物服装、场景、光线和镜头风格，避免单独生成时漂移。
- 不要求生图模型生成中文编号、中文标题、中文招式名或说明文字。
- 招式名和说明只放在“后期文字内容”里。
- 武打类只写影视化攻防画面、错位接触、重心变化和视觉结果，不输出真实格斗教学步骤。

## 工作流程

1. 识别动作类型：徒手、拳脚、擒拿、摔法、兵器、追打、群战、威压出招、仙侠武打或写实动作片。
2. 明确空间条件：双方起始站位、距离、朝向、可移动范围、障碍物、道具或兵器位置。
3. 将结果式描述拆成武打节拍：预备架势 -> 试探或启动 -> 攻击路径 -> 防守或闪避 -> 接触或错位 -> 重心变化 -> 收招或反击。
4. 为每个节拍指定身体层级：眼神锁定、肩胯转动、重心下沉、脚步换位、手臂路线、拳脚落点、兵器轨迹。
5. 写清攻防逻辑：谁先动，攻击从哪里来，被攻击方如何判断、格挡、闪避、借力、反击。
6. 控制镜头时长：短镜头只写一到两个核心招式；复杂连招拆成多个镜头或时间段。
7. 把动作写入原提示词的“人物动作”“画面描述”“场景互动”或对应字段，不另起新结构。

## 改写规则

- 保留用户原有角色、剧情、场景、镜头、台词、比例和输出格式。
- 不直接写“打得很帅、很快、很猛、很有力量”；必须写出发力路径和可见动作。
- 武术动作必须有先后顺序：看见对手 -> 调整架势 -> 脚步启动 -> 身体带动手脚或兵器 -> 攻防接触或错位 -> 重心回收。
- 发力从脚下和腰胯写起，不只写手臂挥动：脚掌蹬地、膝盖微屈、腰胯旋转、肩线跟随、手臂或兵器最后到位。
- 写清步法：前脚试探、后脚跟进、侧步让线、退步卸力、转身换位、交叉步追击。
- 写清攻防方向：从左上、右下、正前、侧后、低位扫来；防守方用哪只手、哪条腿或哪件兵器处理。
- 写清安全错位：影视化假打、镜头错位、擦身而过、衣料或发丝被带动、身体反应承接；不要写真实伤害细节。
- 多人物打斗必须分清主攻者、被动方、旁人位置和下一个威胁来源，避免多人同时乱动。
- 兵器动作必须写持握方式、刃口或棍尖方向、攻击弧线、防守接触点和收势位置。
- 仙侠或特效武打要先有真实身体动作，再叠加灵光、气浪、剑气、符法或飞身效果。
- 默认模式下不堆叠无因果的招式；动作链优先模式下保留用户指定动作，用连续微节拍建立因果，并让多个动作共用一个有动机的主运镜。

## 武打类型

- 徒手对打：写架势、步法、拳路、掌法、肘膝、格挡、闪避、反击和收势。
- 拳脚连招：按“起手 -> 第一击 -> 对方处理 -> 第二击 -> 重心回收”组织，不只列招式名。
- 擒拿挣脱：写抓握点、关节方向、重心压制、对方如何卸力或反制。
- 摔法跌落：写失衡来源、脚步被破坏、身体转向、手臂保护、落点和回弹。
- 兵器对打：写兵器长度、攻击轨迹、格挡角度、碰撞点、震动反应和收招方向。
- 群战：主角每次只处理一个最近威胁，同时用走位避开其他人；不要让所有人同时扑上。
- 追打：写启动、追近、避障、回身反击、距离变化和镜头跟随落点。
- 仙侠武打：身体动作先成立，再加入御剑、法术、气浪、衣袂、尘土或光效响应。

## 输出适配

- 单段视频提示词：返回完整可复制提示词，把武术动作过程自然融入原文。
- 分镜表：保留列名和镜头数，只改“人物动作”“画面描述”“场景互动”等相关字段。
- 时间轴提示词：按秒数写攻防节拍，确保每个招式能在时长内完成。
- 局部修改：只改用户指定武打动作，不重写无关镜头。
- 与 `video-microexpression-enhancer` 同时使用时，武术动作指导负责身法、步法、攻防和接触逻辑；微表情技能负责眼神、呼吸和面部情绪链。
- 与镜头角度设计同时使用时，先确定攻防路径，再让镜头服务关键招式，不让运镜和动作方向互相冲突。

## 质量检查

交付前确认：

- 每个武打动作都有起势、攻击或防守过程、结果和收势。
- 双方站位、距离、攻防方向、视线方向和兵器位置没有冲突。
- 发力路径明确，不是只有手臂或兵器凭空挥动。
- 接触用影视化错位和身体反应表达，没有真实伤害细节。
- 默认模式下动作量符合镜头时长；动作链优先模式下不按数量扣分，改查每个动作是否有明确主体、承受方、结果和下一动作衔接。
- 景别能看清动作重点；特写不承担完整连招，远景不承担细微手指变化。
- 没有改变用户指定事实、台词和格式。

## 简短示例

原句：

`男人冲过去一拳打倒对手。`

增强：

`男人先压低重心，右脚向前半步试探，视线锁住对手胸口；对手抬手准备格挡时，男人左脚蹬地带动腰胯旋转，右肩跟进，右拳从身体中线向对手左侧面门方向打出。镜头用错位表现拳锋擦过对手脸侧，对手头部顺势偏开，肩膀后撤半步，重心失衡向右退开。男人拳头打完后立刻收回到胸前，脚步站稳，保持下一招的防守架势。`
## 10秒 FPV 一镜到底双人格斗分支

当用户要求 8—12 秒双人格斗、FPV 第一视角、随行伙伴式贴身跟拍、一镜到底、无剪辑无转场，或给出按秒拆分的高密度拳脚提示词时，读取 [references/fpv-one-take-two-person-fight.md](references/fpv-one-take-two-person-fight.md)。

- 第一遍先清理乱码和错词，并锁定人物服装、发型、鞋子、起始站位、场地边界与道具位置。
- “FPV 第一视角”和“第三人称伙伴跟拍”只能选择一种，不能在同一镜头中混用。
- 默认将 10 秒控制在 4—6 个主要动作节拍；动作链优先模式不设数量上限，保留全部指定动作并拆成连续微节拍。
- 每句话必须写清动作主体、承受方、左右侧、移动方向、重心结果和摄影机跟随对象。
- 一镜到底不等于持续旋转；每个节拍只设置一个主要运镜。
- 未在开场建立的车辆、路锥、箱体等道具不得中途突然出现。
- 设备、分辨率、帧率和胶片参数仅作为质感补充，优先保证人物连续性、攻防逻辑、空间关系和镜头可执行性。
- 影视接触使用镜头错位、擦身、衣料带动和身体反应表达，不输出真实伤害教学。
