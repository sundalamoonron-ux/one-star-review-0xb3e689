#!/usr/bin/env python3
"""One-Star Review of Something Essential — resubmit 3, sleep line.

This program writes exactly one deadpan one-star review to
/output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt when set).

Why this line
------------
The brief asks for a one-star review of an everyday essential, deadpan,
filed in earnest against something that cannot be fixed. Sleep qualifies:
it is named in the brief itself, everyone relies on it nightly, and nobody
can return it. The line treats sleep as a service with a returns desk —
"takes eight hours" is the setup, "returns a version of me that is still
tired" is the turn, and the sting lands in the last few words, after the
complaint has been read straight. The grievance is the sharpest true one
sleep offers: a full night's sleep that still leaves you tired, a small
daily annoyance everyone recognises but rarely sees written down as a
complaint. It stays deadpan throughout — no exclamation mark, no wink, no
explaining the joke, one joke told cleanly.

Why it replaces the gravity line
---------------------------------
The gravity line ("Gravity works for free, then charges interest every
time I stand up too fast.") scored 532004 (rank 376/2675) in round 2 and
509911 (rank 422/2980) in round 3 — strong, but outside the top 5. In a
three-round pairwise tournament against gravity, judged on the house
criteria in order (funniest, sharpest grievance, deadpan, turn in the last
words, tight and specific), the sleep line won every round by a clear
margin: waking up tired after eight hours is a sharper, more universal
daily grievance than dizziness from standing up too fast, while holding
the deadpan, the turn, and the single-joke shape just as well. The other
finalists (oxygen on stairs, teeth with no warranty, sleep billed by the
hour) only ever beat gravity by a hair, so they stay out. The rest of the
field — sun, Mondays, water, time, Wi-Fi, rain, alarm — lost to gravity
outright, mostly on a weaker grievance or a less canonical essential.

Why the gate matters
--------------------
RULES.txt seals the gate: /output/entry.txt must be UTF-8 text of 1 to 160
characters, not only whitespace. An invalid entry scores Valid 0, never
reaches the judge, and takes no prize. At 72 characters this line sits
comfortably inside the limit, and it is a single line with no line breaks.

Why no trailing newline
-----------------------
The entry is the review text and nothing else. A trailing newline would add
a byte the judge reads as part of the text and would break the "one line"
shape. So the file is written with newline="" and no "\n" appended: the
bytes on disk are exactly the 72 characters of the review.

Self-checks the program performs
---------------------------------
Before writing: the review's length is checked against the 1-160 gate and
rejected if it is whitespace-only or contains a line break. After writing:
the file is read back as raw bytes, decoded as UTF-8 (which also proves it
is valid UTF-8), and compared byte for byte with the review constant. Any
mismatch aborts with a non-zero exit instead of silently leaving a bad entry.
"""

import os
import sys

# The review text, byte for byte. Tournament winner over the gravity line
# (3/3 audit rounds, clear margin on sharpest-grievance criterion).
REVIEW = "Sleep takes eight hours and returns a version of me that is still tired."


def fail(message: str) -> int:
    print(f"gate failed: {message}", file=sys.stderr)
    return 1


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")

    # Pre-write gate: length 1-160, not whitespace-only, single line, and no
    # invisible leading/trailing spaces that would silently change the bytes
    # the judge reads.
    if not 1 <= len(REVIEW) <= 160:
        return fail(f"review is {len(REVIEW)} chars, outside 1-160")
    if not REVIEW.strip():
        return fail("review is whitespace-only")
    if REVIEW != REVIEW.strip():
        return fail("review has leading or trailing whitespace")
    if "\n" in REVIEW or "\r" in REVIEW:
        return fail("review must be a single line")

    os.makedirs(out_dir, exist_ok=True)
    # newline="" plus no appended "\n": bytes on disk == review exactly.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(REVIEW)

    # Post-write verification: read the raw bytes back and compare.
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
