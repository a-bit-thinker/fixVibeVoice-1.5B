#!/usr/bin/env python3
"""Standalone prompt normalizer for multi-speaker scripts.

This file is intentionally independent from the existing codebase so users can
normalize prompts before passing them into any pipeline.
"""

from __future__ import annotations

import re
from typing import List

_SYMBOL_MAP = {
    ":": " colon ",
    ";": " semicolon ",
    ",": " comma ",
    ".": " period ",
    "!": " exclamation point ",
    "?": " question mark ",
    "(": " left parenthesis ",
    ")": " right parenthesis ",
    "&": " and ",
    "@": " at ",
    "%": " percent ",
    "#": " hashtag ",
    "$": " dollar ",
}


def verbalize_symbols(text: str) -> str:
    """Convert punctuation symbols into spoken words."""
    normalized = text
    for symbol, spoken in _SYMBOL_MAP.items():
        normalized = normalized.replace(symbol, spoken)
    return re.sub(r"\s+", " ", normalized).strip()


def normalize_prompt(prompt: str, default_speaker: int = 1) -> str:
    """Normalize prompt lines while preserving speaker envelopes.

    Input formats:
    - "Speaker X: message"
    - plain text (assigned to default_speaker)
    """
    normalized_lines: List[str] = []

    for raw_line in prompt.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        match = re.match(r"^Speaker\s+(\d+)\s*:\s*(.*)$", line, flags=re.IGNORECASE)
        if match:
            speaker_id = int(match.group(1))
            speaker_text = verbalize_symbols(match.group(2))
        else:
            speaker_id = default_speaker
            speaker_text = verbalize_symbols(line)

        if speaker_text:
            normalized_lines.append(f"Speaker {speaker_id}: {speaker_text}")

    if not normalized_lines:
        raise ValueError("No valid content found in prompt")

    return "\n".join(normalized_lines)


if __name__ == "__main__":
    sample = """Speaker 1: Hello: world!\nHow are you?"""
    print(normalize_prompt(sample))
