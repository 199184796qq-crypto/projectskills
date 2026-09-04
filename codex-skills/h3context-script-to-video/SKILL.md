---
name: h3context-script-to-video
description: Convert a Chinese or English script, character references, and timing plan into copy-ready segmented MiniMax H3 Context video prompts. Use for H3 continuous short dramas, script-to-video prompts, multi-segment video generation, airlock continuity, speaker IDs, dialogue tags, soundscape, and background-music evolution.
---

# H3 Context Script to Video

中文注释：h3 长剧本转context提示词

Turn a script into independently usable, continuous MiniMax H3 segment prompts. Output English visual/audio directions while retaining dialogue and visible in-world text exactly as supplied.

## Workflow

1. Extract total runtime, scene, character anchors, dialogue, visible text, BGM beats, and timestamped story beats.
2. Segment by supplied time ranges. Keep each segment 5–15 seconds. Split longer ranges at natural story, dialogue, scene, or BGM boundaries; merge sub-5-second ranges into an adjacent beat.
3. Plan each segment: duration, shots, exact cut times, final-frame state, speakers, sound, and music transition.
4. Write the first segment directly. For every later segment, start with a two-second **airlock**: match the prior segment's final framing, character position, gaze, wardrobe, lighting, and emotion; keep the camera static; use only micro-movements such as breathing, weight shifts, eye movement, or fabric movement; do not use dialogue in this buffer. Change scene or framing only after the buffer.
5. Run the final checklist before responding.

Read [references/source-guideline.md](references/source-guideline.md) when the request needs the complete original specification, uncommon dialogue tags, or detailed camera-motion vocabulary.

## Prompt rules

- Use the script's character wording consistently. On each segment's first appearance of a character, restate the full anchor in this order: hair, face if useful, upper clothing, lower clothing, footwear, accessories, posture/expression. Do not synonym-swap anchor traits.
- Number speakers independently inside each segment: `(S1)`, `(S2)`, and so on.
- For dialogue, preserve original dialogue verbatim inside `<d>[Chinese] ...</d>` or the source-language tag. Do not translate it.
- For an off-screen speaker, write `says in an off-screen voiceover` and immediately state that the on-screen character's lips remain closed. Never describe an off-screen-only character's appearance.
- Use `<scenetrans>` only when a line continues across a cut; use `<cutoff>` only when the segment cuts a line short.
- Use camera motion in natural English: motion type plus amplitude/speed where meaningful, e.g. `The camera pushes in with small amplitude at slow speed.`
- Start Shot 1 by grounding environment, materials, lighting, and space. Quote visible in-world text in English double quotes exactly as provided.
- Scale density to duration: 5–6 seconds = 1–2 shots; 7–10 seconds = 2–3 shots; 11–15 seconds = 3–5 shots. Do not overstuff short segments.
- End every segment on a clearly described final visual state; it becomes the next segment's airlock reference.
- Immediately after each segment's final `[Shot N]` description, add two new standalone lines before `overall_soundscape`, in this exact language-matched order. For Chinese prompts use `画面中不出现任何可读文字：无字幕、无台词字幕、无文字叠层、无 UI、无标签、无 Logo、无水印、无片尾文字。所有对白仅以角色口述声音呈现，画面不显示台词文字。` then `全片不准出现字幕。`; for English prompts use `No readable on-screen text: no subtitles, dialogue captions, text overlays, UI text, labels, logos, watermarks, or end credits. All dialogue is heard only and is never displayed as text.` then `No subtitles are allowed throughout the video.` Do not omit, reword, move, or turn either line into another shot.
- Describe `overall_soundscape` in 1–4 English sentences: room tone, physical sounds, nonverbal human sounds, and reverb. Do not repeat dialogue.
- Describe `non_diegetic_music` in 1–3 English sentences: instruments, BPM/rhythm when known, energy curve, and explicit relation to the previous segment's music. Use `N/A` when absent.

## Required output format

Return only the prompt blocks, separated by a standalone `===` line with blank lines around it. Do not add explanations unless the user asks.

```text
## 段N（对应成片 00:00–00:08）— 节拍简述
& 8 &
integrated_multimodal_description: [Shot 1] Live-action, cinematic, ...

overall_soundscape: ...

non_diegetic_music: ...
```

Use segment-relative timestamps: the first shot has no timestamp; every later shot uses `At 00:SS.mmm`. Do not put `===` after the last segment.

## Final check

- Verify segment durations sum to the requested total and each is 5–15 seconds.
- Verify each block has all three required fields and its `& integer &` duration line.
- Verify all later segments use the two-second airlock before any major change.
- Verify character anchors, speaker behavior, dialogue tags, visible text, and BGM evolution remain continuous.
- Verify every segment places the two language-matched standalone lines directly after its final shot and before `overall_soundscape`: the complete no-readable-text constraint first, then the no-subtitles rule.
