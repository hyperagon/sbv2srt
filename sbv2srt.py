#!/usr/bin/env python3
"""Convert a YouTube-style .sbv subtitle file to .srt."""

import argparse
import re
from pathlib import Path

TIMESTAMP_LINE = re.compile(
    r"^\s*(\d{1,2}:\d{2}:\d{2}[.,]\d{3})\s*,\s*"
    r"(\d{1,2}:\d{2}:\d{2}[.,]\d{3})\s*$"
)


def to_srt_timestamp(timestamp: str) -> str:
    return timestamp.replace(".", ",")


def convert_sbv_to_srt(text: str) -> str:
    # Split into non-empty blocks. Each SBV block starts with a start,end line,
    # followed by one or more lines of subtitle text.
    blocks = re.split(r"\n\s*\n", text.strip())
    srt_blocks = []

    for block in blocks:
        lines = block.splitlines()
        if not lines:
            continue

        match = TIMESTAMP_LINE.match(lines[0])
        if not match:
            raise ValueError(f"Invalid SBV timestamp line: {lines[0]!r}")

        start, end = match.groups()
        subtitle_text = "\n".join(lines[1:])

        srt_blocks.append(
            f"{len(srt_blocks) + 1}\n"
            f"{to_srt_timestamp(start)} --> {to_srt_timestamp(end)}\n"
            f"{subtitle_text}"
        )

    return "\n\n".join(srt_blocks) + ("\n" if srt_blocks else "")


def main():
    parser = argparse.ArgumentParser(description="Convert an SBV subtitle file to SRT.")
    parser.add_argument("input", type=Path, help="Input .sbv file")
    parser.add_argument(
        "output", nargs="?", type=Path,
        help="Output .srt file (defaults to the input filename with .srt extension)",
    )
    args = parser.parse_args()

    output_path = args.output or args.input.with_suffix(".srt")
    sbv_text = args.input.read_text(encoding="utf-8-sig")
    output_path.write_text(convert_sbv_to_srt(sbv_text), encoding="utf-8")

    print(f"Converted {args.input} to {output_path}")


if __name__ == "__main__":
    main()
