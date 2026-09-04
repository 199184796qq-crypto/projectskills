---
name: volcengine-api
description: 火山引擎 API 集成技能，包含“语音技能”和“视频技能”。当用户要求使用火山API、豆包语音、Volcengine TTS、文本转语音、配音、旁白、语音生成、音频生成、火山视频生成、Seedance、文生视频、图生视频、视频接口检测、视频 dry-run 或生成 MP4 时使用。生成类远程请求执行前必须展示请求内容、参数和费用估算，等待用户明确确认后才可提交。
---

# 火山 API

## 分类

当前能力分类：

- 语音技能：火山/豆包 TTS，文本生成 MP3。
- 视频技能：火山/Seedance 视频生成、视频资源检测、dry-run、MP4 生成。

## 语音生成流程

1. 读取 `references/voice-tts.md`，确认接口、参数、计费和错误处理。
2. 明确文本来源、输出路径、声音要求、语速、音量、音高、目标时长和是否只要干净人声。已有上下文足够时不要重复提问。
3. 提交前展示以下内容并等待用户明确回复“确认提交”或同等授权：
   - 完整口播文本
   - 声音提示词
   - 模型与 endpoint
   - `audio_config` 参数
   - 预估时长与当前计费规则
   - 预估费用公式
4. 未获得确认时，只能预览请求，不得调用远程生成。测试、重试、重生也必须重新确认。
5. 从 `VOLCENGINE_TTS_API_KEY` 读取密钥；允许读取当前进程、Windows 用户环境变量或机器级环境变量。不得把 API Key 写入技能、项目文件、命令输出或响应文件。
6. 使用 `scripts/generate_voice_tts.py` 生成 MP3，并保存脱敏响应 JSON。
7. 生成后用 `ffprobe` 或等效工具核对文件格式、采样率、声道和实际时长。
8. 最终报告模型、`duration`、计费用的 `original_duration`、计费规则、预估费用、音频路径和响应路径。

## 视频生成流程

1. 读取 `references/video-generation.md`，确认认证、profile、模型/endpoint、dry-run、真实生成和轮询规则。
2. 检测或排障时优先执行只读/不扣费命令：`arkcli auth status`、`arkcli profile show`、`arkcli resources list --modality video`、`arkcli models search seedance`、`arkcli +gen --dry-run ...`。
3. 如果控制面报缺少 Volc SSO STS，先按 `arkcli auth login volc-sso` 或 `arkcli auth login --no-browser` 完成 SSO；如果缺少 profile，经用户确认后创建 `platform` profile。
4. 真实视频生成前必须展示 prompt、模型或 endpoint、比例、时长、分辨率、是否生成音频、保存位置、预计费用/计费口径，并等待用户明确回复“确认提交”或同等授权。
5. 真实视频生成默认使用异步任务；提交后报告 `task_id/status`，用 `arkcli gen get <task_id>` 轮询，成功后报告本地 MP4 路径。
6. 不要把 `dry-run` 当成真实连通成功；`dry-run` 只证明本地命令和参数构造通过。只有真实提交并返回任务 ID 才能证明数据面生成接口已接受任务。

## 路径规则

输出路径由具体项目决定。本技能负责火山语音与视频 API 调用。

如果用户提到“杨鸭子”，先按 `yyzdouyin-copywriter` 的归档规则确定项目目录；音频保存到 `配音` 子目录，视频保存到 `视频` 子目录。

## 错误处理

- `Invalid X-Api-Key`：停止重试，提示用户提供豆包语音新版控制台的 `X-Api-Key`；不要用方舟 API Key 替代。
- `requires Volc SSO STS`：说明控制面认证缺少 SSO，走火山 SSO 登录后重试。
- `profile "default" not found`：说明本地 profile 缺失；经用户确认后创建 `platform` profile，再重试资源查询。
- 远程接口返回错误：保存脱敏响应，报告 HTTP 状态、接口 code、logid 和响应路径。
- 本地生成失败：不要伪造成功文件；明确说明未生成音频。

## 中文名称与说明

- 中文名称：火山 API
- 用途说明：火山引擎 API 集成技能，包含“语音技能”和“视频技能”。当用户要求使用火山API、豆包语音、Volcengine TTS、文本转语音、配音、旁白、语音生成、音频生成、火山视频生成、Seedance、文生视频、图生视频、视频接口检测、视频 dry-run 或生成 MP4 时使用。生成类远程请求执行前必须展示请求内容、参数和费用估算，等待用户明确确认后才可提交。
