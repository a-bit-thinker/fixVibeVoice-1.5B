#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PATH="${VENV_PATH:-/root/fish-venv-cu126}"
MODEL_PATH="${MODEL_PATH:-$ROOT_DIR/checkpoints/VibeVoice-1.5B}"
TOKENIZER_PATH="${TOKENIZER_PATH:-$ROOT_DIR/checkpoints/Qwen2.5-1.5B-tokenizer}"
HOST="${HOST:-0.0.0.0}"
PORT="${PORT:-7861}"
DEVICE="${DEVICE:-cuda}"
ALLOW_BGM_VOICES="${ALLOW_BGM_VOICES:-0}"
LOG_DIR="${LOG_DIR:-$ROOT_DIR/logs}"
LOG_KEEP="${LOG_KEEP:-20}"
APP_VERSION="$(cat "$ROOT_DIR/VERSION" 2>/dev/null || echo "dev")"

if [[ ! -d "$VENV_PATH" ]]; then
  echo "Virtualenv not found: $VENV_PATH"
  exit 1
fi

if [[ ! -d "$MODEL_PATH" ]]; then
  echo "Model directory not found: $MODEL_PATH"
  exit 1
fi

if [[ ! -d "$TOKENIZER_PATH" ]]; then
  echo "Tokenizer directory not found: $TOKENIZER_PATH"
  exit 1
fi

source "$VENV_PATH/bin/activate"
cd "$ROOT_DIR"

mkdir -p "$LOG_DIR"
ts="$(date +%Y%m%d-%H%M%S)"
safe_version="$(echo "$APP_VERSION" | tr -c 'A-Za-z0-9._-' '_')"
LOG_FILE="$LOG_DIR/vibevoice_${safe_version}_${ts}.log"
ln -sfn "$(basename "$LOG_FILE")" "$LOG_DIR/latest.log"

if [[ "$LOG_KEEP" =~ ^[0-9]+$ ]] && (( LOG_KEEP > 0 )); then
  mapfile -t stale_logs < <(
    ls -1t "$LOG_DIR"/vibevoice_*.log 2>/dev/null | tail -n +"$((LOG_KEEP + 1))"
  )
  if (( ${#stale_logs[@]} > 0 )); then
    rm -f "${stale_logs[@]}"
  fi
fi

exec > >(tee -a "$LOG_FILE") 2>&1

echo "Starting VibeVoice LAN server on ${HOST}:${PORT}"
echo "Version: $APP_VERSION"
echo "Model: $MODEL_PATH"
echo "Tokenizer: $TOKENIZER_PATH"
echo "Device: $DEVICE"
echo "Log file: $LOG_FILE"
echo "Latest log: $LOG_DIR/latest.log"

extra_args=()
if [[ "$ALLOW_BGM_VOICES" == "1" ]]; then
  extra_args+=(--allow_bgm_voices)
fi

python demo/gradio_demo.py \
  --model_path "$MODEL_PATH" \
  --tokenizer_path "$TOKENIZER_PATH" \
  --device "$DEVICE" \
  --host "$HOST" \
  --port "$PORT" \
  "${extra_args[@]}"
