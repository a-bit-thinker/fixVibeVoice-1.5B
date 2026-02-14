#!/usr/bin/env python3
"""CLI utility to verbalize symbols in text for more stable TTS output."""

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from vibevoice.processor.text_normalizer import verbalize_symbols


def main() -> None:
    parser = argparse.ArgumentParser(description="Replace symbols with oral names.")
    parser.add_argument("--text", type=str, help="Raw input text.")
    parser.add_argument("--input", type=Path, help="Optional input text file path.")
    parser.add_argument("--output", type=Path, help="Optional output file path.")
    args = parser.parse_args()

    if bool(args.text) == bool(args.input):
        raise SystemExit("Please provide exactly one of --text or --input")

    raw_text = args.text if args.text is not None else args.input.read_text(encoding="utf-8")
    normalized_text = verbalize_symbols(raw_text)

    if args.output:
        args.output.write_text(normalized_text, encoding="utf-8")
    else:
        print(normalized_text)


if __name__ == "__main__":
    main()
