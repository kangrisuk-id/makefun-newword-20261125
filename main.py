#!/usr/bin/env python3
"""Write the invented word entry for the "Invent a Word We Need" bounty.

The entry is the invented word plus its one-line definition. This program
holds the entry, writes it to /output/entry.txt, and honours $MAKEFUN_OUTPUT_DIR
when set, then validates the file: non-empty, one line, no CR/LF, at most 140
characters, UTF-8 encodable.
"""

import os
import sys
from pathlib import Path

# The entry: the invented word plus its one-line definition.
WORD = "draftlimbo"
DEFINITION = "the typed messages you left abandoned in drafts, where no one expects them to be found."

ENTRY = f"{WORD} — {DEFINITION}"

MAX_CHARS = 140


def output_dir() -> Path:
    """The directory the entry is written to: $MAKEFUN_OUTPUT_DIR when set, else /output."""
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return Path(env_dir) if env_dir else Path("/output")


def validate(entry: str) -> None:
    """Raise ValueError when the entry breaks the gate's rules."""
    if not entry or not entry.strip():
        raise ValueError("entry is empty")
    if "\n" in entry or "\r" in entry:
        raise ValueError("entry must be one line, with no CR/LF")
    if len(entry) > MAX_CHARS:
        raise ValueError(f"entry is {len(entry)} characters, at most {MAX_CHARS} allowed")
    entry.encode("utf-8")


def main() -> int:
    validate(ENTRY)
    target = output_dir() / "entry.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    if target.read_text(encoding="utf-8") != ENTRY:
        raise ValueError("written entry does not match the held entry")
    print(f"wrote {target} ({len(ENTRY)} characters)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
