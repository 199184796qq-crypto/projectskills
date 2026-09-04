# 语音技能：火山/豆包 TTS

## 已验证接口

- Endpoint: `POST https://openspeech.bytedance.com/api/v3/tts/create`
- 鉴权请求头: `X-Api-Key`
- 请求追踪头: `X-Api-Request-Id`，每次使用新 UUID
- 模型: `seed-audio-1.0`
- API Key 来源: 豆包语音新版控制台的 API Key 管理；方舟 API Key 不可替代

## 默认声音

通用电商口播默认声音：

> 年轻的抖音电商女声，普通话，自然亲切，有食欲感，像真实分享好吃的东西。不要播音腔，不要夸张叫卖。语速相对较快，节奏干净利落。只输出干净人声，不要背景音乐、环境音和音效。

根据具体文案补充 2 至 3 个需要重读的用户感知点。不要把制作工艺当作重读卖点。

## 默认音频参数

- `format`: `mp3`
- `sample_rate`: `24000`
- `speech_rate`: `10`
- `loudness_rate`: `5`
- `pitch_rate`: `0`
- `enable_subtitle`: `true`
- 默认不添加显式或隐式水印

## 计费与审批

- 豆包音频生成模型 1.0 按返回的 `original_duration` 计费；不要用处理后的 `duration` 计算。
- 2026-07-10 观察到的公开后付费价格为 1 元/分钟。价格可能变化，每次提交前优先核对官方计费页。
- 估算公式: `original_duration / 60 × 当前每分钟单价`。
- 每次远程提交、测试、重试或重新生成前，都要展示完整请求与费用估算并获得用户明确确认。

## 脚本用法

预览请求，不提交远程接口：

```powershell
python scripts/generate_voice_tts.py `
  --preview-request `
  --text-file '<项目>\文案\文案.txt' `
  --output '<项目>\配音\配音.mp3' `
  --response '<项目>\配音\配音_响应.json'
```

确认后提交：

```powershell
python scripts/generate_voice_tts.py `
  --confirm-submit `
  --text-file '<项目>\文案\文案.txt' `
  --output '<项目>\配音\配音.mp3' `
  --response '<项目>\配音\配音_响应.json'
```

不要在命令输出、对话或文件中显示真实 API Key。

脚本读取顺序：当前进程环境变量 `VOLCENGINE_TTS_API_KEY`，Windows 用户环境变量，Windows 机器级环境变量。
