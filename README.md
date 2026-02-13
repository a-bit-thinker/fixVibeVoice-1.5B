It's hard to imagine all code just finish by codex within 2 days, it fix aroud 100 conflict and error occur whole workflow. all the things I do is just vibing(vibing for coding)lol. and I don't believe any human engineer can finish these scripts and conlicts in 1 mouth without ai. you need read too much readme (totally 129,343,616 cached and output=298,488 (reasoning 163,994))
# VibeVoice LAN Shell (Fork)

GitHub-ready fork of Microsoft VibeVoice focused on practical local/LAN TTS usage with a stable WebUI workflow.

Current release: `v0.2.0`

## Upstream

- Upstream project: https://github.com/microsoft/VibeVoice
- This fork keeps upstream core model code and adds deployment/debug improvements for local server use.

## What This Fork Adds

- `run_lan.sh` launcher with versioned logs and `latest.log` symlink.
- Local tokenizer/model loading defaults for offline or semi-offline workflows.
- More robust uploaded audio loading path (browser recordings included).
- Voice clone upload panel in WebUI.
- Single-speaker, dry-speech prompting (less random music/sound effects).
- Generation thread isolation/cleanup for repeated WebUI runs.
- Voice conditioning cap for long uploaded clone samples to reduce sample-content leakage.
- Clearer progress accounting (`text_tokens` + `voice_prompt_tokens`) in logs.

## Tested Environment

- Ubuntu 22.04+
- Python 3.10
- NVIDIA GPU (CUDA)
- Virtualenv (example: `/root/fish-venv-cu126`)

## Quick Start

### 1) Clone and install

```bash
cd /root/fish-speech
git clone https://github.com/<your-user>/VibeVoice.git
cd VibeVoice

python3 -m venv /root/fish-venv-cu126
source /root/fish-venv-cu126/bin/activate

pip install --upgrade pip
pip install -e .
```

### 2) Download checkpoints

```bash
source /root/fish-venv-cu126/bin/activate
cd /root/fish-speech/VibeVoice

# Main TTS model
hf download microsoft/VibeVoice-1.5B --local-dir checkpoints/VibeVoice-1.5B

# Tokenizer used by this setup
hf download Qwen/Qwen2.5-1.5B --local-dir checkpoints/Qwen2.5-1.5B-tokenizer
```

If `hf` asks for login:

```bash
hf auth login
```

Use a valid Hugging Face token from https://huggingface.co/settings/tokens

### 3) Launch WebUI on LAN

```bash
cd /root/fish-speech/VibeVoice
source /root/fish-venv-cu126/bin/activate

HOST=0.0.0.0 PORT=7861 ./run_lan.sh
```

Open from another device on same network:

```text
http://<server-lan-ip>:7861
```

## Runtime Controls

`run_lan.sh` supports:

- `VENV_PATH` (default `/root/fish-venv-cu126`)
- `MODEL_PATH` (default `checkpoints/VibeVoice-1.5B`)
- `TOKENIZER_PATH` (default `checkpoints/Qwen2.5-1.5B-tokenizer`)
- `HOST` (default `0.0.0.0`)
- `PORT` (default `7861`)
- `DEVICE` (default `cuda`)
- `ALLOW_BGM_VOICES` (`0` or `1`)
- `LOG_DIR` (default `logs`)
- `LOG_KEEP` (default `20`)

Example:

```bash
HOST=0.0.0.0 PORT=7861 DEVICE=cuda LOG_KEEP=50 ./run_lan.sh
```

## Voice Clone Behavior (Important)

This fork intentionally caps long uploaded clone audio during conditioning to reduce the bug where sample speech content leaks into generated output.

Defaults:

- `VIBEVOICE_MAX_CLONE_SECONDS=30`
- `VIBEVOICE_CLONE_SEGMENTS=3`

Tune if needed:

```bash
export VIBEVOICE_MAX_CLONE_SECONDS=40
export VIBEVOICE_CLONE_SEGMENTS=4
./run_lan.sh
```

Guidance:

- Best naturalness usually comes from clean speech with one speaker.
- Longer than ~30s can improve timbre stability but may increase style/content leakage.
- If leakage appears, lower `VIBEVOICE_MAX_CLONE_SECONDS`.

## Troubleshooting

### Tokenizer load error

If you see `Can't load tokenizer for 'Qwen/Qwen2.5-1.5B'`, verify local path exists:

```bash
ls checkpoints/Qwen2.5-1.5B-tokenizer
```

And run with the correct path:

```bash
TOKENIZER_PATH=/root/fish-speech/VibeVoice/checkpoints/Qwen2.5-1.5B-tokenizer ./run_lan.sh
```

### `flash_attn` install failure

`flash_attn` is optional. This fork falls back to SDPA automatically if unavailable.

### Mobile cannot open page

Use HTTP on LAN (`http://...`). Local self-signed HTTPS often fails on mobile browsers.

### Progress looks confusing

This fork logs progress basis in WebUI output:

- `text_tokens`
- `voice_prompt_tokens`

This is clearer than raw prompt-length denominators for long clone prompts.

## Release Notes

### v0.2.0

- Fixed long clone sample leakage by adding conditioning cap and segment selection.
- Improved generation progress accounting and log clarity.
- Improved repeated-run stability with generation thread cleanup.
- Kept LAN and logging workflow from `v0.1.0`.

## Tag and Push to GitHub

```bash
cd /root/fish-speech/VibeVoice
git add VERSION README.md ROLLBACK.md demo/gradio_demo.py vibevoice/modular/modeling_vibevoice_inference.py vibevoice/processor/vibevoice_processor.py
git commit -m "release: vibevoice shell v0.2.0"
git tag -a v0.2.0 -m "VibeVoice LAN shell v0.2.0"
git push origin main --tags
```

## License

This repo remains under the upstream license (`LICENSE`). Review upstream policy and applicable laws before deploying voice generation systems.
