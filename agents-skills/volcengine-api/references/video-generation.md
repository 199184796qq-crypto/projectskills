# 视频技能：火山/Seedance 视频生成

## 已验证本机状态

- CLI: `arkcli`
- 认证方式: 火山 SSO + ARK API Key
- 已创建默认 profile: `platform_cn-beijing_default`
- profile 类型: `platform`
- region: `cn-beijing`
- project: `default`
- base_url: `https://ark.cn-beijing.volces.com/api/v3`
- 当前可用视频 endpoint:
  - `ep-20260710010525-8xvsz`
  - `ep-20260710005706-xj4dr`

这些值是 2026-07-10 检测结果。后续使用时先用只读命令刷新确认。

## 检测流程

只做连通性检测时，不提交真实生成任务：

```powershell
arkcli auth status
arkcli profile show
arkcli resources list --modality video
arkcli models search seedance
arkcli +gen --dry-run --model ep-20260710010525-8xvsz --modality video --duration 4 --ratio 9:16 --resolution 720p "连通性测试，不提交生成"
```

判断口径：

- `auth status` 成功且 `logged_in=true`：本地认证存在。
- `resources list --modality video` 成功返回 items：控制面资源查询通。
- `models search seedance` 成功返回模型：模型目录查询通。
- `+gen --dry-run` 返回 `validated=true`：本地命令、模型/endpoint 和参数构造通过。
- `dry-run` 不会证明真实生成数据面已接受任务；真实提交返回 `task_id` 才能证明生成接口已接受任务。

## 常见模型

优先用当前 profile 的视频 endpoint；需要模型名时可用：

- `doubao-seedance-2-0-fast-260128`
- `doubao-seedance-2-0-260128`
- `doubao-seedance-2-0-mini-260615`
- `doubao-seedance-1-5-pro-251215`

使用模型名生成前先查参数：

```powershell
arkcli models get doubao-seedance-2-0-fast --transform supported_params
```

`doubao-seedance-2-0-fast` 常用参数边界：

- `resolution`: `480p` 或 `720p`
- `ratio`: `16:9`, `4:3`, `1:1`, `3:4`, `9:16`, `21:9`, `adaptive`
- `duration`: 4 到 15 秒，或 `-1`
- `priority`: 0 到 9
- `generate_audio`: 支持，默认 true
- `watermark`: 支持，默认 false
- 不支持 `draft`、`frames`、`camera_fixed`

## 真实生成审批

真实生成视频前必须展示：

- prompt
- 使用的 endpoint 或模型
- `modality=video`
- `duration`
- `ratio`
- `resolution`
- `generate_audio`
- `watermark`
- `save_to`
- 当前计费口径和预计费用

只有用户明确回复“确认提交”或同等授权后，才可执行不带 `--dry-run` 的生成命令。重试、重生、测试生成也要重新确认。

## 真实生成与轮询

提交异步视频任务：

```powershell
arkcli +gen --model ep-20260710010525-8xvsz --modality video --duration 4 --ratio 9:16 --resolution 720p --save-to "<输出目录>" "<prompt>"
```

返回 `task_id` 后轮询：

```powershell
arkcli gen get <task_id> --save-to "<输出目录>"
```

成功后报告：

- `task_id`
- `status`
- `local_path`
- 模型或 endpoint
- 时长、比例、分辨率
- 费用/用量信息，若返回中存在

## 认证与 profile 修复

如果报：

`requires Volc SSO STS`

走 SSO：

```powershell
arkcli auth login volc-sso
```

如果浏览器 SSO 的 `redirect_uri` 失败，走无浏览器两段式：

```powershell
arkcli auth login --no-browser
arkcli auth login --no-browser --code <授权码>
```

如果报：

`profile "default" not found`

经用户确认后创建 profile：

```powershell
arkcli profile create --type platform --region cn-beijing --project default --set-default --no-interactive
```

## Windows 本地参考图 URL（优先方式，已更正）

- **强制默认**：用户提供 Windows 本地图片作为视频参考图时，直接使用 `file:///C:/...`；不要先改写为 data URI，也不要重复测试其他 `file://` 变体。
- 正确绝对路径写法是 `file:///C:/Users/19918/Downloads/reference.png`；盘符前必须是三条 `/`，路径一律使用正斜杠。
- 多图原始请求中，将该 URL 直接写入：`{type:"image_url", role:"reference_image", image_url:{url:"file:///C:/.../reference.png"}}`。SDK 会自动上传本地文件。
- `file://C:\Users\...`、`file://C:/Users\...`、相对路径都不正确。文件名含空格时使用 `%20`，例如 `file:///C:/Users/19918/Downloads/a%20b.png`。
- 使用 `arkcli +gen` 时，本地图片可写 `--input @C:/Users/19918/Downloads/reference.png`，它会构造同样的绝对 `file:///C:/...` URL；多图可重复 `--input`，或按需要使用 `reference_image:@C:/...`。
- 本节优先级高于下方旧的 data-URI 兜底说明：先用本节的 `file:///` 方式；只有确定当前 CLI/SDK 版本无法上传时，才采用 data URI 兜底。

## Windows 多图参考图稳定传图（已验证）

适用：Windows 本机文件作为 Seedance 的人物、服装、场景等多张参考图。

- Windows 本地参考图优先用 `file:///C:/...` 绝对 URL，或在 `+gen` 中用 `--input @C:/...`。不要写成 `file://C:\...`；那种盘符与反斜杠混写会被错误解析。
- 在已完成认证、模型/参数确认且用户已确认提交后，直接向 `https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks` 发起同一数据面请求。使用环境变量 `ARK_API_KEY` 的 Bearer 鉴权；不得打印、保存或写入密钥。
- 读取本地图片后仅在内存中处理：转为 RGB JPEG，最长边限制在 `1280px`，以 `quality=90` 编码，再转成 `data:image/jpeg;base64,...`。不要把 base64 放进命令行参数、日志或工作区文件。
- 请求体使用 `content` 数组：先放 `{type:"text", text:<prompt>}`；每张参考图放 `{type:"image_url", role:"reference_image", image_url:{url:<data-uri>}}`。提示词中必须明确每张图的职责，例如“图1只作人物、图2只作服装、图3只作场景”，防止资产串用。
- 该链路已经成功创建并完成任务；后续同类 Windows 多图任务直接复用，不必为了验证路径再做 `file://` 或 `--input` 试跑。提交后仍按正常流程用 `arkcli gen get <task_id> --save-to <dir> --open` 轮询并下载。
- 如果服务端返回 `InputImageSensitiveContentDetected.PrivacyInformation`，表示输入图被判定为可能含真实人像；任务不会创建。应请用户换成明确的 AI 虚拟人物/去识别化素材，或经用户同意移除人物参考后再提交；不要对同一组被拦截素材重复测试。

该命令会写入本机 arkcli 配置，因此执行前需要用户确认。
