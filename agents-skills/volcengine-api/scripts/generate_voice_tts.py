#!/usr/bin/env python3
"""Generate MP3 voice audio with Volcengine Seed Audio after explicit approval."""

from __future__ import annotations

import argparse
import base64
import json
import os
from pathlib import Path
import urllib.error
import urllib.request
import uuid


API_URL = "https://openspeech.bytedance.com/api/v3/tts/create"
MODEL = "seed-audio-1.0"
DEFAULT_VOICE_PROMPT = (
    "年轻的抖音电商女声，普通话，自然亲切，有食欲感，像真实分享好吃的东西。"
    "不要播音腔，不要夸张叫卖。语速相对较快，节奏干净利落。"
    "只输出干净人声，不要背景音乐、环境音和音效。"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--preview-request", action="store_true")
    mode.add_argument("--confirm-submit", action="store_true")
    parser.add_argument("--text-file", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--response", type=Path, required=True)
    parser.add_argument("--voice-prompt", default=DEFAULT_VOICE_PROMPT)
    parser.add_argument("--speech-rate", type=int, default=10)
    parser.add_argument("--loudness-rate", type=int, default=5)
    parser.add_argument("--pitch-rate", type=int, default=0)
    return parser.parse_args()


def fail(message: str, **details: object) -> None:
    print(json.dumps({"ok": False, "message": message, **details}, ensure_ascii=False))
    raise SystemExit(1)


def get_api_key() -> str | None:
    api_key = os.environ.get("VOLCENGINE_TTS_API_KEY")
    if api_key or os.name != "nt":
        return api_key

    try:
        import winreg
    except ImportError:
        return None

    registry_locations = (
        (winreg.HKEY_CURRENT_USER, r"Environment"),
        (
            winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment",
        ),
    )
    for root, path in registry_locations:
        try:
            with winreg.OpenKey(root, path) as key:
                value, _ = winreg.QueryValueEx(key, "VOLCENGINE_TTS_API_KEY")
        except OSError:
            continue
        if value:
            return str(value)
    return None


def build_payload(args: argparse.Namespace, text: str) -> dict[str, object]:
    return {
        "model": MODEL,
        "text_prompt": f"{args.voice_prompt}\n\n口播内容：\n{text}",
        "audio_config": {
            "format": "mp3",
            "sample_rate": 24000,
            "speech_rate": args.speech_rate,
            "loudness_rate": args.loudness_rate,
            "pitch_rate": args.pitch_rate,
            "enable_subtitle": True,
        },
        "watermark": {
            "aigc_watermark": False,
            "aigc_metadata": {"enable": False},
        },
    }


def main() -> None:
    args = parse_args()
    if not args.preview_request and not args.confirm_submit:
        fail("缺少 --preview-request 或 --confirm-submit；未向火山提交请求。")

    text = args.text_file.read_text(encoding="utf-8").strip()
    if not text:
        fail("文案为空；未向火山提交请求。")

    payload = build_payload(args, text)

    if args.preview_request:
        print(
            json.dumps(
                {
                    "ok": True,
                    "submitted": False,
                    "endpoint": API_URL,
                    "model": MODEL,
                    "payload": payload,
                    "output": str(args.output),
                    "response": str(args.response),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    api_key = get_api_key()
    if not api_key:
        fail("未配置 VOLCENGINE_TTS_API_KEY；未向火山提交请求。")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.response.parent.mkdir(parents=True, exist_ok=True)

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Api-Key": api_key,
            "X-Api-Request-Id": str(uuid.uuid4()),
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            status = response.status
            headers = dict(response.headers)
            body = response.read()
    except urllib.error.HTTPError as exc:
        status = exc.code
        headers = dict(exc.headers)
        body = exc.read()

    result = json.loads(body.decode("utf-8"))
    safe_result = {key: value for key, value in result.items() if key != "audio"}
    args.response.write_text(
        json.dumps(safe_result, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    logid = headers.get("X-Tt-Logid") or headers.get("x-tt-logid")
    if status >= 300 or result.get("code") not in (None, 0):
        fail(
            result.get("message") or "火山接口请求失败。",
            status=status,
            code=result.get("code"),
            logid=logid,
            response=str(args.response),
        )

    if result.get("audio"):
        args.output.write_bytes(base64.b64decode(result["audio"]))
    elif result.get("url"):
        urllib.request.urlretrieve(result["url"], args.output)
    else:
        fail("火山响应中没有音频数据或下载地址。", response=str(args.response))

    print(
        json.dumps(
            {
                "ok": True,
                "model": MODEL,
                "audio": str(args.output),
                "duration": result.get("duration"),
                "original_duration": result.get("original_duration"),
                "logid": logid,
                "response": str(args.response),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
