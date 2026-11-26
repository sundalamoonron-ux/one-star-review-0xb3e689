#!/usr/bin/env python3
"""One-Star Review of Something Essential — gravity.

Writes a single deadpan one-star review line to /output/entry.txt.
Gate (RULES.txt): UTF-8 text, 1-160 characters, not only whitespace.
"""
import os
import sys

LINE = "One star for gravity. Reliable, yes, but it never once asked if I wanted to come down."

def main() -> int:
    if not (1 <= len(LINE) <= 160):
        print(f"gate failed: line is {len(LINE)} chars, must be 1-160", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("gate failed: line is whitespace only", file=sys.stderr)
        return 1
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(LINE)
    # Read-back verification: the written file must be byte-identical
    # to the line, one single line, and still inside the 1-160 gate.
    with open("/output/entry.txt", "r", encoding="utf-8") as f:
        written = f.read()
    assert written == LINE, "read-back mismatch: entry.txt differs from LINE"
    assert "\n" not in written, "read-back failed: entry must be a single line"
    assert 1 <= len(written) <= 160, "read-back failed: gate 1-160 chars"
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
