#!/usr/bin/env python3
"""One-Star Review of Something Essential — gravity (revert 2).

Writes exactly one deadpan one-star review to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when set).

My reasoning for this line
--------------------------
The brief wants a one-star review, filed in earnest, against an everyday
essential that cannot be fixed. Gravity is the strongest candidate: it is
universal, nobody can opt out, and complaining about it is obviously
futile — which is exactly what makes a deadpan one-star review of it
funny. Framing it as a service with a billing department gives the line
its shape: "works for free" is the setup (it sounds generous), "then
charges interest every time I stand up too fast" is the turn (the hidden
cost arrives as a bill). The sting is a true, shared annoyance — standing
up too fast genuinely makes you dizzy — so the complaint reads as a real
grievance, not a joke about a joke. No exclamation mark, no wink, no
punchline label: the deadpan tone is what sells it.

I verified this exact line independently against the repo's own history
(commit 6d88af1, the original main.py): the wording is byte-identical,
77 characters, and it is the line that scored 532004 (round 2) and 509911
(round 3), well above the Monday replacement line that scored only
378753 in round 4. Reverting restores the proven line.

The gate
---------
RULES.txt: /output/entry.txt must be UTF-8, 1-160 characters, not only
whitespace. At 77 characters this line sits safely inside the gate, and
it is a single line with no line breaks.

No trailing newline
-------------------
The entry is the review text and nothing else. A trailing newline would
add a byte the judge reads as part of the text and would break the
one-line shape, so the file is written with newline="" and no "\n".

Self-checks in this program
---------------------------
Before writing: length 1-160, not whitespace-only, no leading/trailing
whitespace, single line. After writing: read the raw bytes back, decode
as UTF-8 (proving valid UTF-8), and compare byte for byte with the review
constant. Any mismatch exits non-zero instead of leaving a bad entry.
"""

import os
import sys

# The review, byte for byte. Verified against commit 6d88af1 in this repo.
REVIEW = "Gravity works for free, then charges interest every time I stand up too fast."


def fail(message: str) -> int:
    print(f"gate failed: {message}", file=sys.stderr)
    return 1


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")

    # Pre-write gate checks.
    if not 1 <= len(REVIEW) <= 160:
        return fail(f"review is {len(REVIEW)} chars, outside 1-160")
    if not REVIEW.strip():
        return fail("review is whitespace-only")
    if REVIEW != REVIEW.strip():
        return fail("review has leading or trailing whitespace")
    if "\n" in REVIEW or "\r" in REVIEW:
        return fail("review must be a single line")

    os.makedirs(out_dir, exist_ok=True)
    # newline="" and no appended "\n": bytes on disk == review exactly.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(REVIEW)

    # Post-write verification: raw bytes round-trip.
    with open(path, "rb") as f:
        data = f.read()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return fail("entry.txt is not valid UTF-8")
    if text != REVIEW:
        return fail("written text differs from the review")
    if not 1 <= len(text) <= 160:
        return fail(f"written entry is {len(text)} chars, outside 1-160")
    if "\n" in text:
        return fail("written entry is not a single line")

    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
