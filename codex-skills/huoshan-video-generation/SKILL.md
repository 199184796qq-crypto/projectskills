---
name: huoshan-video-generation
description: Use this when the user says "使用火山生成视频" or asks to generate a video with 火山/火山方舟/Ark/Seedance. It enforces an approval-first workflow before any remote Volcengine generation call.
---

# Huoshan Video Generation

Use this skill only when the user explicitly says "使用火山生成视频" or clearly asks to generate a video through 火山/火山方舟/Ark/Seedance.

## Core Rules

- Prefer 火山 Ark CLI (`arkcli`) for video generation.
- Use the installed CLI's actual command surface: current `@volcengine/ark-cli` uses `arkcli +gen`; do not invent or substitute `arkcli image-to-video` / `--input-image` unless the local `arkcli --help` explicitly provides them.
- Use the locally configured Ark CLI platform profile. The user's preferred API key is already configured in the local profile; do not print the full key in user-facing responses.
- Never submit a remote generation request immediately.
- Any remote call that may generate, test-generate, retry, dry-run remotely, or incur cost requires explicit user approval first.
- Only submit after the user clearly replies `确认提交` or an equivalent explicit approval.
- If the user has not approved yet, do not run `arkcli +gen`.
- Before every submission, ask the user where to save the downloaded video. This question is mandatory every time. If the user does not provide a new directory, use the previous save directory.
- After submitting a remote video generation request, return the task ID to the user as soon as it is available. Do not wait until the video finishes before reporting the task ID. Continue waiting for completion afterward, then report the final local path, usage, and cost estimate.

## Windows local reference images

When `arkcli +gen --input @<Windows path>` produces a malformed `file://D:\...` URI or a local-file parse error, use this verified workaround:

1. Copy or stage the images under a short ASCII directory such as `D:\ark_inputs`.
2. Pass root-relative file URLs with forward slashes and no `@` or drive letter, for example:

```powershell
--input "reference_image:file:///ark_inputs/person.png"
--input "reference_image:file:///ark_inputs/package.png"
--input "reference_image:file:///ark_inputs/bite.png"
```

On Windows, `/ark_inputs/person.png` resolves to `D:\ark_inputs\person.png` when the CLI runs from the D: volume. Verify the files exist before submission. Do not place the local paths in the prompt text; `--input` is the actual multimodal upload channel.

For three reference images, use explicit `reference_image:` roles so the first image is not implicitly treated as the video first frame. Keep the prompt's image mapping in the same order: person, package, product-after-bite.

The current CLI does not support `arkcli image-to-video` or repeated `--input-image` flags unless its local help output says otherwise. Use repeated `--input` flags with `arkcli +gen`.

## Required Flow

1. First identify the generation mode before asking for model or prompt details. Ask the user to choose one:
   - **文生视频**：只提供文字提示词，不上传参考素材。
   - **首帧图生视频**：一张图片作为视频首帧，再按提示词生成运动。
   - **首尾帧生视频**：分别提供首帧和尾帧，生成两帧之间的过渡视频。
   - **多图参考生视频**：多张图片分别作为人物、产品、场景或细节参考，不把它们误当成首尾帧。
   - **多模态生视频**：组合图片、视频、音频等输入，并逐项确认每个素材的角色。
   - **文生图**：先确认用户是只要图片，还是要“先文生图，再把生成图片作为首帧继续生视频”；前者转图片流程，后者按两阶段流程执行。

   Do not infer the mode from the number of uploaded files. Confirm the intended role of every input before submission.

2. When triggered for video, list video model options for the user to choose.
   - Prefer Ark CLI model/resource discovery when available.
   - If Ark CLI cannot list models because SSO control-plane access is unavailable, use the known Seedance model candidates below and say that control-plane listing requires SSO.

3. Ask for details step by step, not all at once.
   - Ask one decision at a time where possible.
   - Use concise numbered options.
   - Do not ask about camera movement unless the user brings it up.

4. Required details before submission:
   - Model
   - Video content/prompt
   - Ratio: `9:16`, `16:9`, or `1:1`
   - Duration
   - Resolution if supported/needed
   - Background music / environment sound / speech / subtitles
   - Audio choice and subtitle choice, then inject those choices into the final prompt's trailing `必须约束条件`
   - Visual style
   - Reference assets: none, reference image, reference video, or reference audio
   - Confirmed generation mode and the role/order of every reference asset
   - Output save directory. Ask every time before submission. If the user does not specify one, reuse the previous save directory.

5. Before submission, show the final planned request:
   - Model ID
   - Prompt
   - Ratio
   - Duration
   - Resolution
   - Audio settings
   - Subtitle settings
   - The final prompt must end with `必须约束条件`, including the user's confirmed audio and subtitle choices
   - Reference inputs
   - Output save directory
   - Pricing rule and estimated cost if enough information is available

6. Ask the user to reply `确认提交`.

Before submitting, ask the user to confirm or change the output save directory every time.

7. Only after explicit confirmation, submit through Ark CLI.

8. After submission, immediately report the task ID once the CLI response exposes it, then continue monitoring the same task until it succeeds or fails.

## Prompt constraint injection

Before showing the final request, normalize the user's audio and subtitle choices into a short `必须约束条件` block at the very end of the prompt. Do this even when the user already described audio or subtitles elsewhere, so the model receives the constraints in the strongest position.

Use explicit wording:

- If the user wants no subtitles: `必须约束条件：不要生成字幕，不要文字贴片，不要文字气泡。`
- If the user wants subtitles: `必须约束条件：生成与口播一致的中文字幕，字幕不要遮挡人物、产品或关键动作。`
- If the user wants no background music: add `不要背景音乐，不要广告配乐。`
- If the user wants speech: add the exact speech/voice requirement, such as `保留人物自然口播，嘴型与中文台词同步。`
- If the user wants environment sound or product sound: add the concrete sounds, such as `保留真实室内环境底噪、轻微撕包装声、轻微咬脆皮声。`

If the user has not chosen audio or subtitles yet, ask before finalizing the prompt. Do not submit a video request with ambiguous audio/subtitle constraints.

## Mode-to-input mapping

Use the selected mode to build the `--input` list:

| Mode | Input mapping |
|---|---|
| 文生视频 | No `--input` flags |
| 首帧图生视频 | One `first:` image input |
| 首尾帧生视频 | `first:` image followed by `last:` image |
| 多图参考生视频 | Explicit `reference_image:` for each image; do not let the first image become an unintended first frame |
| 多模态生视频 | Explicit `reference_image:`, `reference_video:`, and/or `reference_audio:` roles according to the user's mapping |

For Windows local assets, combine these roles with the verified root-relative URL workaround, such as `first:file:///ark_inputs/start.png`, `last:file:///ark_inputs/end.png`, or `reference_image:file:///ark_inputs/person.png`.

## Model Options

Use current models if Ark CLI can list them. Known candidates:

- `doubao-seedance-2-0-fast-260128`
- `doubao-seedance-2-0-260128`
- `doubao-seedance-2-0-mini-260615`
- `doubao-seedance-1-5-pro-251215`
- `doubao-seedance-1-0-pro-fast-251015`
- `doubao-seedance-1-0-pro-250528`

If the user selects a short display name such as `doubao-seedance-2-0-fast`, resolve to the full versioned model ID before submission. Previously, the short ID failed while `doubao-seedance-2-0-fast-260128` succeeded.

## Ark CLI Submission Pattern

Use `arkcli +gen` only after approval. Example shape:

```powershell
arkcli +gen --model <model-id> --modality video --ratio <ratio> --duration <seconds> --save-to <dir> --wait --open "<prompt>" --format json
```

If the user requested no auto-open, omit `--open`.

Use a stable local save directory, usually:

```text
D:\yangduck_video_work
```

## Cost Reporting

After every successful generation, report:

- Model
- Task ID
- Local file path
- Returned usage, especially `usage.total_tokens`
- Pricing rule
- Estimated cost
- Note that actual billing depends on Volcengine console billing, resource packs, coupons, and discounts

Public pricing observed on 2026-07-10 for Seedance 2.0 / 2.0 Fast:

- Without video input: `46 CNY / 1,000,000 tokens`
- With video input: `28 CNY / 1,000,000 tokens`

Formula:

```text
estimated_cost = usage.total_tokens / 1_000_000 * unit_price
```

If token usage is not returned, say cost cannot be calculated exactly from the response and provide the pricing rule.

## Safety

- Do not reveal full API keys, signed URLs beyond what is necessary, or secrets.
- Do not run destructive configuration commands unless the user explicitly asks.
- If the Ark CLI reports SSO is required for listing resources/models, do not start SSO automatically unless the user asks; continue with known model candidates and explain the limitation.
