#!/usr/bin/env python3
"""One-Star Review of Something Essential.

Writes one deadpan one-star review (at most 160 characters) of an everyday
essential to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The review: Monday, framed as an appointment nobody made and nobody can
cancel — the one weekly meeting with no unsubscribe button.
"""

import os
import sys

REVIEW = "Monday is the only appointment I never made and still cannot cancel."


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")

    # Self-check the gate before writing: 1-160 chars, not whitespace-only.
    if not 1 <= len(REVIEW) <= 160:
        print(f"gate failed: {len(REVIEW)} chars", file=sys.stderr)
        return 1
    if not REVIEW.strip():
        print("gate failed: whitespace-only", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    # No trailing newline: the entry is exactly the review text, 68 chars.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(REVIEW)
    os.chmod(path, 0o644)

    # Verify after write: exact bytes, one line, gate holds.
    with open(path, "rb") as f:
        data = f.read()
    text = data.decode("utf-8")
    assert text == REVIEW, "written text differs from review"
    assert 1 <= len(text) <= 160, "gate failed after write"
    assert text.strip(), "gate failed after write (whitespace-only)"
    assert "\n" not in text, "entry must be a single line"
    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
