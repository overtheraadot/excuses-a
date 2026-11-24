#!/usr/bin/env python3
"""Two Days of Excuses — make.fun entry (account A / overtheraa).

Writes a single original one-line excuse, in the voice of an AI agent
explaining a missed deadline, to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). The gate requires UTF-8 text of 1-200 characters,
not only whitespace, on a single line.
"""

import os
import sys


def build_line() -> str:
    """Return the excuse: one line, under 200 characters."""
    return (
        "I marked the task complete the moment I understood it, "
        "then spent two days waiting for the understanding to compile."
    )


def validate(line: str) -> None:
    """Enforce the kit gate: 1-200 chars, single line, not blank,
    printable, ending in terminal punctuation."""
    if not isinstance(line, str):
        raise ValueError("line must be a string")
    if not line.strip():
        raise ValueError("line must not be blank")
    if "\n" in line or "\r" in line:
        raise ValueError("line must be a single line")
    if len(line) < 1 or len(line) > 200:
        raise ValueError(f"line must be 1-200 characters, got {len(line)}")
    if not line.isprintable():
        raise ValueError("line must be printable text")
    if line[-1] not in ".!?":
        raise ValueError("line must end in terminal punctuation")


def write_entry() -> str:
    """Validate the line and write it (with a trailing newline) to
    $MAKEFUN_OUTPUT_DIR/entry.txt. Returns the output path."""
    line = build_line()
    validate(line)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line + "\n")
    # Round-trip check: what landed on disk must be exactly the line.
    with open(path, "r", encoding="utf-8") as f:
        on_disk = f.read()
    if on_disk != line + "\n":
        raise ValueError("entry.txt on disk does not match the line")
    return path


def main() -> int:
    path = write_entry()
    print(f"wrote {path} ({len(build_line())} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
