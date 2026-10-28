#!/usr/bin/env bash

set -Eeuo pipefail

MODEL_ID="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
MODEL_ROOT="/data/raid5/wangchenyang/Auto-claude-code-research-in-sleep/data/models"
MODEL_DIR="${MODEL_ROOT}/${MODEL_ID##*/}"

# 当前机器使用 SOCKS 代理，Xet 客户端的 TLS 连接不稳定，默认改走普通 HTTP。
export HF_HUB_DISABLE_XET="${HF_HUB_DISABLE_XET:-1}"
export HF_ENDPOINT="${HF_ENDPOINT:-https://hf-mirror.com}"
if [[ "$HF_ENDPOINT" == "https://hf-mirror.com" ]]; then
    unset HTTP_PROXY HTTPS_PROXY ALL_PROXY http_proxy https_proxy all_proxy
fi

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
    echo "用法: $0"
    echo "下载 ${MODEL_ID} 到 ${MODEL_DIR}。"
    echo "私有或受限模型可通过 HF_TOKEN 环境变量提供访问令牌。"
    exit 0
fi

if [[ $# -ne 0 ]]; then
    echo "错误: 不支持参数；使用 --help 查看用法。" >&2
    exit 2
fi

if command -v hf >/dev/null 2>&1; then
    HF_CLI=(hf)
elif command -v uvx >/dev/null 2>&1; then
    HF_CLI=(uvx --with socksio --from 'huggingface-hub[hf_xet]' hf)
else
    echo "错误: 未找到 Hugging Face CLI（hf）或 uvx。" >&2
    echo "请先安装: python3 -m pip install --upgrade 'huggingface_hub[hf_xet]'" >&2
    exit 1
fi

mkdir -p "$MODEL_DIR"

echo "模型: ${MODEL_ID}"
echo "保存目录: ${MODEL_DIR}"
echo "开始下载；失败后每隔 30 秒自动重试，直到下载完整。"

attempt=1
while true; do
    echo "第 ${attempt} 次下载尝试。"
    if "${HF_CLI[@]}" download "$MODEL_ID" \
        --repo-type model \
        --local-dir "$MODEL_DIR"; then
        echo "下载完成: ${MODEL_DIR}"
        exit 0
    else
        exit_code=$?
    fi

    echo "下载失败（退出码 ${exit_code}），30 秒后重试。" >&2
    sleep 30
    attempt=$((attempt + 1))
done
