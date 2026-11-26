"""The Painfully Honest Out-of-Office.

The entry is a single out-of-office auto-reply. This program writes that
line, and only that line, to ``entry.txt`` inside the grader's output
directory (``MAKEFUN_OUTPUT_DIR``, default ``/output``).

Design:
- One constant line, 146 characters, one sentence: a "Thank you" opening
  keeps it warm and manager-safe, then the painful confession — the sender
  will reply on return just as soon as the inbox has been cleared by
  deleting everything too polite to delete. Politeness itself is the reason
  emails get deleted: a private truth no employee admits in public.
- Deterministic by construction: no randomness, no clock, no network, no
  input. Two runs write byte-identical files.
- Standard library only (``os``, ``pathlib``).
- The file holds the line with no trailing newline, so the judged text is
  exactly the line.
"""

import os
from pathlib import Path

# The auto-reply: 146 characters, a single sentence.
LINE = (
    "Thank you for your email \u2014 I'm away and will reply on my return, "
    "just as soon as I've deleted everything I was too polite to delete "
    "before I left."
)


def main() -> None:
    # Guard the gate at runtime: the sealed scorer only accepts 1-200
    # characters, a single non-blank line. Fail loudly rather than submit
    # an invalid entry if the line is ever edited past the limit.
    if not 1 <= len(LINE) <= 200:
        raise ValueError(f"reply line is {len(LINE)} characters, must be 1-200")
    if "\n" in LINE or not LINE.strip():
        raise ValueError("reply line must be one non-blank line")
    # Criterion 4 of the judge's brief: one sentence. The line must end in
    # exactly one full stop and contain no other sentence terminator.
    if LINE.count(".") != 1 or not LINE.endswith("."):
        raise ValueError("reply line must be exactly one sentence")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    entry_path = out_dir / "entry.txt"
    entry_path.write_text(LINE, encoding="utf-8")


if __name__ == "__main__":
    main()
