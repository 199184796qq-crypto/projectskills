---
name: sales-video-copy-cases
description: Collect, analyze, retrieve, and adapt Chinese short-video sales copy cases for Douyin, Kuaishou, Xiaohongshu, Qianchuan ads, food/product demos, spoken scripts, hooks, audience variants, promotion copy, and direct ready-to-shoot ecommerce video scripts. Use when the user asks for 带货文案, 口播文案, 短视频销售文案, 千川素材, 卖货脚本, 爆款开头, 食品试吃文案, 多受众版本, 收录带货案例, or wants a product copy case adapted from saved examples.
---

# Sales Video Copy Cases

## Core Rule

Return production-ready Chinese copy. Do not over-explain when the user asks for usable copy.

When the user asks to create or adapt copy:

1. Read `references/copy-case-library.md` first when available.
2. Match the product and desired effect to saved cases by hook, audience, product category, tone, and conversion goal.
3. Break down the matched case before adapting it: hook, pain point, product proof, sensory words, price/offer, urgency, call to action.
4. Preserve user-provided nouns, prices, product names, audience groups, regional wording, and platform constraints exactly.
5. Treat duration, line count, and screenshot/page format as hard production constraints.
6. Convert merchant-facing selling points into user-facing pain points, needs, visible proof, and felt benefits before writing the final script.
7. Present `卖点翻译` as a Markdown table by default.
8. Run the final copy through `references/compliance-check.md`.
9. Add a `生成图片提示词` from `references/copy-image-prompt.md` after the copy. This image prompt is only for turning the spoken copy text into a text-only image; mark keywords inside the spoken text itself, include tone/expression cues inline, and attach visual shooting suggestions only to key selling-point sentences or segments.
10. Output direct final copy unless the user asks for analysis.
11. Always include a final `合规检查` report stating advertising-law and Douyin ecommerce risks, replacements made, and any claims the user must verify.

For requests about `爆款开头`, `开头公式`, `起量开头`, `机制类开头`, or `薅羊毛开头`, read `references/viral-opening-formulas.md`.

For requests about `可视化卖点`, `S级卖点`, `A级卖点`, `B级卖点`, `功能性展示`, `预防性视角`, or `结果性视角`, read `references/visual-selling-point-cases.md`.

For every final sales-copy output, read or apply `references/compliance-check.md` before answering.

For every generated spoken sales copy, read or apply `references/copy-image-prompt.md` and include a final `生成图片提示词` before `合规检查`.

## Selling Point Translator

When the user or client provides selling points, do not copy them from the merchant's self-satisfied perspective. Translate each selling point through this chain:

```text
商家卖点 -> 用户听不懂/不关心的原因 -> 用户痛点/需求 -> 可视化证据 -> 口播表达
```

Use these translation questions:

- `这跟用户有什么关系？`
- `用户会在哪个场景里需要它？`
- `它解决了什么麻烦、顾虑、尴尬、浪费、疼点、馋点或不方便？`
- `镜头里怎么证明它？`
- `用户听完能不能立刻想象到好处？`

Default outputs should avoid bare product terms such as `食品级材质`, `PBT刷毛`, `传统工艺`, `甄选原料`, `升级配方`, `高端品质`, unless they are followed by the user-facing result. For example:

```text
食品级材质 -> 给孩子用、孕期用、入口接触更放心
PBT刷毛 -> 不容易滋生细菌、刷着不扎牙龈、牙龈敏感也能用
传统卤制工艺 -> 味道进到肉里、骨边肉也入味、不是表面有味
真空包装 -> 家里囤着方便、拆开就能吃、送人不尴尬
```

## Collecting Cases

When the user says `收录`, `学习这个文案`, `保存这个案例`, or provides a sales script as a style sample:

1. Store or update the case in `references/copy-case-library.md`.
2. Extract `触发词`, `适用产品`, `目标人群`, `文案结构`, `商家卖点`, `用户痛点/需求`, `可视化卖点`, `口感/质感词`, `价格机制`, `成交动作`, and `禁用/注意项`.
3. Record what made the copy work, not just the final wording.
4. If the case depends on visuals, product state, actor tone, local dialect, or holiday context, record those external conditions.
5. Ask briefly for missing essentials only when they change the copy: product, audience, price/offer, platform, duration, or required tone.

Never store full cases, examples, or reusable scripts in this `SKILL.md`. Keep this file as workflow instructions only. Put every case in `references/copy-case-library.md` or another clearly named file under `references/` to save context tokens.

## Case Display Format

When listing or recommending a saved case, do not simply paste the old script.

Use:

1. `案例匹配原因` - why this case fits.
2. `卖点翻译` - merchant selling point -> user pain/need -> visible proof -> spoken phrase.
3. `文案拆解` - hook, scene, pain/desire, product proof, sensory description, offer, urgency, CTA.
4. `重点标注` - key words or rhythm that must be preserved.
5. `可替换变量` - product, audience, scene, price, quantity, activity, CTA.
6. `套用建议` - how to adapt without losing the effect.
7. `最终文案` - one directly usable script or the requested number of variants.

## Copy Structure

Default structure for food/product short videos:

```text
钩子：一句话抓住好奇、反差、痛点或强体验。
场景：谁在什么场景需要它。
卖点：1-2个最强卖点，别堆参数。
感官：口感、质地、香味、使用感、画面感。
证明：实拍动作、手持展示、拆开/咬开/使用过程、用户视角。
价格/活动：价格、数量、限时、福利。
催单：自然口语收尾，适合直播间、链接或评论区转化。
```

## Output Defaults

- Use spoken Chinese, short sentences, and mouth-friendly rhythm.
- Prefer one strong final script over many weak options.
- For multiple audiences, write separate versions instead of one universal script.
- For food, use concrete sensory words: 香、糯、嫩、脆、软烂、入味、爆汁、绵密、回甘, but avoid fake medical or exaggerated claims.
- For local products, preserve local scene and spoken flavor.
- If the user asks for `直接给我文案`, output only the final copy.

## Format Options

If not specified, use:

```markdown
【标题/用途】
【适用人群】
【卖点翻译】
| 商家卖点 | 用户真正关心 | 可视化证明 | 口播表达 |
| --- | --- | --- | --- |
【口播文案】
...
【拍摄提示】
...
【生成图片提示词】
...
【合规检查】
...
```

For Qianchuan or ad material, use:

```markdown
【人群】
【开头3秒】
【正文口播】
【画面动作】
【转化收口】
【备注】
```

## Compliance

Avoid absolute claims such as 全网最低, 治疗, 根治, 永久有效, 100%有效, 必瘦, 必赚. Replace with experience-based wording like 我吃着觉得, 适合, 可以试试, 口感更像, 家里囤着方便. Final answers must include the `合规检查` report from `references/compliance-check.md`.

## 中文名称与说明

- 中文名称：销售视频文案案例库
- 用途说明：销售视频文案案例的收集、分析、检索与改写。
