---
name: h3-prompt-writing
description: Write MiniMax H3 video generation prompts for T2VA, I2VA, FL2VA, L2VA, and Ref2VA. Use when rewriting multimodal requests into H3 prompt structures, composing integrated_multimodal_description, overall_soundscape, and non_diegetic_music, aligning keyframes, or defining reference labels for images, videos, and audio.
---

# H3 Prompt Writing

## Input Asset Intake Gate

Run this intake before choosing an H3 mode or writing any prompt.

1. If the user invokes this skill without attaching or listing assets, first ask whether they have character images, scene images, prop images, first/last frames, reference videos, or voice/audio assets to upload. Pause prompt generation until they answer or explicitly choose to proceed without assets.
2. If assets are already attached or listed in the current request, do not ask the generic upload question again. Inventory the supplied assets and map each one to the script using all available evidence together: the filesystem filename, displayed image/audio name, the user's explicit numbering or description, visible image content, and the narrative role required by the script.
3. Treat the user's explicit mapping as authoritative. For example, if the user states that Picture 1 is a named character or Audio 2 is a named character's voice reference, preserve that relationship across every section and label.
4. Never guess an ambiguous mapping. If two assets could represent the same role, a filename conflicts with the visible content or user description, or the intended subject cannot be identified confidently, ask the user which asset maps to which character, scene, prop, frame, video, or voice before writing the final prompt.
5. Detect missing required inputs from the requested mode and story. Ask specifically for what is missing, such as a referenced character image, environment image, first/last frame, source video, or named speaker's voice reference. Do not invent an asset, reference label, or source relationship to fill the gap.
6. Audio assets are used only in the mode the user assigns: either a character-exclusive voice asset or a segment-wide multi-speaker dialogue asset. A voice-reference asset supplies voice identity only unless the user explicitly authorizes reuse of its words, performance, timing, ambience, or music.
7. Before final output, verify that every referenced asset has one stable label and one unambiguous role, and that every label used in the prompt resolves to an asset actually supplied by the user.

## Workflow

1. Identify the input mode: T2VA, I2VA, FL2VA, L2VA, or full-reference Ref2VA.
2. For base text/keyframe modes, read `references/base-en.txt` and follow its final prompt structure.
3. For full-reference mode, read `references/ref-en.txt` and follow its six-section rewrite format.
4. Preserve the exact field names, section order, labels, and timing notation from the selected guide.

## Dialogue Audio Modes and Binding (Highest-Priority Output Rule)

Every spoken line requires a concrete user-supplied audio asset. Before writing, identify and preserve one user-declared mode for each dialogue source or time range; never infer, silently convert, or bind the same line to both modes. If a segment contains both modes, the user must define their mutually exclusive speaker or time-range coverage.

1. **Character-exclusive voice mode:** each speaking character has a dedicated voice asset. Keep the visual subject, speaker, and audio indices aligned: `<Subject N>` speaks as `(SN)` and uses `<Audio N>`. For example, `<Subject 1>` uses `(S1)` and `<Audio 1>`. Each `<Audio N>` is a voice-timbre reference unless the user explicitly says to copy its original audio.
2. **Segment-wide multi-speaker audio mode:** one supplied `<Audio N>` contains the completed voices, line order, timing, and speaker changes for every speaking character in this segment. Describe it as one standalone `fully_copy` or user-specified `reference` asset in `subject_definitions`, name every contained speaker and their `(SN)`, and state that H3 must preserve the source's speaker identity and lip-sync each visible speaker to that track. Do not fabricate separate per-character audio labels in this mode.

In both modes, every audio asset must receive its own standalone `<Audio N>` definition in `subject_definitions`; never bury an audio description inside a long `<Subject N>` paragraph. Repeat the same audio mode and label in `retention_analysis` and in every spoken `[Shot N]`. In a spoken shot, write the speaker as `<Subject N> (SN)`, state the applicable `<Audio N>` binding and whether it is character-exclusive or segment-wide, then place the complete words in `<d>[Chinese] ...</d>` without interruption.

If a required voice asset or segment-wide dialogue track is absent, stop before producing the final H3 prompt and ask for it or an explicit instruction to remove or rewrite the line. Do not silently substitute a generic AI voice, omit the `<Audio N>` label, or convert an unprovided voice into unlabelled narration.

## Dialogue Tag Contiguity Rule

For every spoken line, keep the speaker identity, `(SN)`, `<Audio N>` binding, speaking verb, and complete `<d>[Chinese] ...</d>` content contiguous in one uninterrupted clause. Do not insert another subject, lip-state instruction, camera instruction, action, or explanatory phrase between the speaker's voice binding and its `<d>` text. Put any required lip-state or performance instruction before that clause or after the closing `</d>` instead. For example, write the silent listener's closed-lip state before the speaker clause, then write the complete speaker clause without interruption.

## User-Fixed Revision Header

For this user's H3 prompt revisions, include a traceable version header in every final deliverable. Use `【第N集｜第M场｜第K段 Vx.y】` as the first line of the H3 prompt block, followed by the segment title on the next line. Use `V1.0` for a first draft and increment the minor version for every user-requested revision. Do not silently overwrite or omit the version identifier unless the user explicitly changes this rule.

## Global Visual Style Inheritance Rule

When a project has an approved global visual-style version, treat it as an immutable master baseline. Repeat its film type, visual style, color relationship, texture, face-lighting target, and prohibitions consistently in every prompt. Scene-specific time, practical lights, ambient-light direction, and supplemental fill may only implement that master baseline; they may never restyle, weaken, replace, or contradict it. Create and use a new global-style version only after the user explicitly changes the global style.

For 《假意家人》, use the approved V1.0 baseline: realistic urban family suspense drama; 9:16; realistic cinematic style with normal straight perspective and domestic scale; low-saturation neutral-natural palette; daytime based on off-white, beige, wood, pale brown, and blue-grey; warm-white interiors rather than orange-gold filters; deep-blue exterior night with restrained warm-white interior contrast; invisible large soft facial fill that preserves real skin texture, eye catchlights, and clothing detail; prohibit black faces, dead eye sockets, clipped highlights, silhouette lighting, studio glare, light-direction jumps, cyber neon, influencer filters, background reconstruction, and furniture drift.

## Base Modes

- T2VA: build the full audiovisual timeline from text.
- I2VA: start from the first frame and develop forward from it.
- FL2VA: describe the continuous path between the first and last frames.
- L2VA: infer a plausible opening and converge to the supplied last frame.

Use `integrated_multimodal_description`, `overall_soundscape`, and `non_diegetic_music` in the order shown in `references/base-en.txt`.

## Full-Reference Mode

Ref2VA rewrites use `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`, `overall_soundscape`, and `non_diegetic_music` in that order. Reference labels stay consistent across all sections.

Read `references/ref-en.txt` for label rules, retention analysis, and complete examples.

## 全片禁字幕固定收尾规则

无论使用 T2VA、I2VA、FL2VA、L2VA 还是 Ref2VA，镜头正文中的最后一个 `[Shot N]` 描述结束后，必须立刻另起两行，按提示词正文语言依次追加完整禁文字约束和固定禁字幕规则。中文提示词依次用 `画面中不出现任何可读文字：无字幕、无台词字幕、无文字叠层、无 UI、无标签、无 Logo、无水印、无片尾文字。所有对白仅以角色口述声音呈现，画面不显示台词文字。` 与 `全片不准出现字幕。`；英文提示词依次用 `No readable on-screen text: no subtitles, dialogue captions, text overlays, UI text, labels, logos, watermarks, or end credits. All dialogue is heard only and is never displayed as text.` 与 `No subtitles are allowed throughout the video.`

- 基础模式将这两句依次放在 `integrated_multimodal_description` 的最后一个镜头之后、`overall_soundscape` 之前；Ref2VA 将其依次放在 `detailed_description` 的最后一个镜头之后、`overall_soundscape` 之前。
- 不得省略、改写、移到其他字段、段落外或另写成一个镜头；中文提示词不得出现英文规则，英文提示词不得保留中文规则。
- 这是一条全片画面规则：禁止字幕、台词字幕、说明文字、UI 文字、片尾文字、水印及任何可读画面文字。

## Output Rules

- Write rewrite sections in English; preserve dialogue, lyrics, and visible scene text in their original language.
- Describe each shot by composition, subjects, environment, actions, camera, sound, and the exact point where referenced content appears.
- Avoid plot summaries, unresolved reference labels, and timing that does not match the requested duration.
- Before delivery, verify that the two language-matched standalone rules directly follow the final `[Shot N]` in the applicable shot-description field, in this order: the complete no-readable-text constraint, then `全片不准出现字幕。` for Chinese prompts or `No subtitles are allowed throughout the video.` for English prompts.
