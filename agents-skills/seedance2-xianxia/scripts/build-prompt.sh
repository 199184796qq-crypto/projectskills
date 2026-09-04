#!/usr/bin/env bash
# Seedance2 仙侠提示词快速组装脚本
# 用法: bash build-prompt.sh <角色> <场景> <动作> <镜头> <色调>

ROLE="${1:-"a young woman in flowing white robes"}"
SCENE="${2:-"above a sea of golden clouds"}"
ACTION="${3:-"rides a luminous jade sword soaring"}"
CAMERA="${4:-"camera follows from a low angle, then sweeps into a wide aerial shot"}"
TONE="${5:-"soft golden hour lighting, ethereal atmosphere"}"
STYLE="Cinematic xianxia style, 4K quality."

PROMPT="${ROLE} ${ACTION} ${SCENE}. The ${CAMERA}. ${TONE}. ${STYLE}"

echo "=== Seedance2 Prompt ==="
echo "$PROMPT"
echo ""
echo "=== 字数统计 ==="
echo "$PROMPT" | wc -w | xargs -I{} echo "{} words"
