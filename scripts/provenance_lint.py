#!/usr/bin/env python3
"""
provenance_lint — keep asserted claims distinguishable from findings.

This repo's docs are written declaratively so the method stays consistent. The
failure mode that creates is silent: a sentence like "blind passes always run
first" enters as one person's design stance, and two commits later it is
indistinguishable from something that was measured. docs/LIMITATIONS.md exists to
hold that line, and it only works if new claims arrive with their provenance.

Two checks:

  TABLE   every row of the provenance table in docs/LIMITATIONS.md has a valid
          status and an evidence pointer that resolves on disk.

  DIFF    normative claims ADDED by this change set are accompanied by a change
          to the provenance table. Diff-scoped on purpose: re-scanning settled
          prose on every commit produces noise nobody reads, and a gate people
          learn to ignore is worse than no gate.

WARN-ONLY by default. Pass --strict to exit non-zero. Do not make this blocking
until its precision has been measured on real commits — see --measure.

Usage:
    python3 scripts/provenance_lint.py                 # staged changes
    python3 scripts/provenance_lint.py --range HEAD~3..HEAD
    python3 scripts/provenance_lint.py --measure       # precision over history
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LIMITATIONS = REPO / "docs" / "LIMITATIONS.md"

VALID_STATUS = {"measured", "single-study", "borrowed", "asserted"}

# Where prose becomes doctrine. Code comments are excluded: they explain a
# mechanism to whoever is editing it, not a claim to whoever is following it.
WATCHED = (
    lambda p: p.startswith("docs/") and p.endswith(".md") and "LIMITATIONS" not in p,
    lambda p: p.startswith("skills/") and p.endswith(".md"),
    lambda p: p.startswith("agents/") and p.endswith(".md"),
    lambda p: p == "README.md",
)

# A normative claim tells a reader what is true or what they must do. These are
# the shapes that carry doctrine; hedged and first-person lines are not claims.
NORMATIVE = re.compile(
    r"\b("
    r"always|never|must(?: not)?|cannot|may not|required|requires|"
    r"is the only|are the only|the whole point|by design|"
    r"is not negotiable|non-negotiable"
    r")\b",
    re.I,
)

# Lines that look normative but are not making a claim about the method.
EXEMPT = re.compile(
    r"^\s*(?:[-*+]\s*)?(?:```|\||#{1,6}\s|>\s*\*\*|<!--)"      # code, tables, headings, callouts
    r"|^\s*\d+\.\s*$"
    r"|\b(?:usage|example|e\.g\.|see |refer to|load |run )\b"    # instructions to the reader
    r"|^\s*[-*+]?\s*`[^`]+`\s*[-—:]"                             # CLI/flag documentation
    r"|`--?[a-z][\w-]*`"                                          # names a flag
    r"|`persona [a-z]"                                             # names a command
    r"|\bthe (?:CLI|validator|schema|scaffold)\b"                  # describes tool behavior
    r"|\bexit (?:0|1|non-zero)\b",
    re.I,
)

# A claim that names its own provenance inline needs no table row.
INLINE_PROVENANCE = re.compile(
    r"\b(asserted|unvalidated|unverified|"
    r"(?:never|not|nothing (?:has|had)|no \w+ (?:has|have)) (?:been )?(?:measured|tested|verified|checked|validated|compared|calibrated)|"
    r"single[- ]study|no evidence|hypothesis|simulated|"
    r"this project's (?:opinion|position|stance)|LIMITATIONS\.md)\b",
    re.I,
)


def git(*args):
    return subprocess.run(["git", "-C", str(REPO), *args],
                          capture_output=True, text=True).stdout


def parse_table():
    """Rows of the provenance table. Returns (rows, errors)."""
    if not LIMITATIONS.exists():
        return [], [f"{LIMITATIONS.relative_to(REPO)} is missing — the provenance table is the whole mechanism"]
    rows, errors = [], []
    in_table = False
    for i, line in enumerate(LIMITATIONS.read_text(encoding="utf8").splitlines(), 1):
        if line.startswith("| Claim | Status | Evidence |"):
            in_table = True
            continue
        if in_table:
            if not line.startswith("|"):
                break
            if set(line) <= set("|- "):
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 3:
                errors.append(f"LIMITATIONS.md:{i}: expected 3 columns, got {len(cells)}")
                continue
            claim, status, evidence = cells
            if status not in VALID_STATUS:
                errors.append(
                    f"LIMITATIONS.md:{i}: status {status!r} is not one of {sorted(VALID_STATUS)}")
            if evidence != "none" and not (REPO / evidence).exists():
                errors.append(
                    f"LIMITATIONS.md:{i}: evidence path does not resolve: {evidence}")
            rows.append({"claim": claim, "status": status, "evidence": evidence, "line": i})
    if in_table and not rows:
        errors.append("LIMITATIONS.md: provenance table parsed to zero rows")
    return rows, errors


def watched(path):
    return any(f(path) for f in WATCHED)


def added_claims(diff_range):
    """Normative lines ADDED by the change set, as (path, text)."""
    args = ["diff", "--unified=0"]
    args += [diff_range] if diff_range else ["--cached"]
    out = git(*args)
    claims, path = [], None
    for line in out.splitlines():
        if line.startswith("+++ b/"):
            path = line[6:]
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        if not path or not watched(path):
            continue
        text = line[1:].strip()
        if not text or EXEMPT.search(text) or len(text) < 25:
            continue
        if not NORMATIVE.search(text):
            continue
        if INLINE_PROVENANCE.search(text):
            continue
        claims.append((path, text))
    return claims


def table_touched(diff_range):
    args = ["diff", "--name-only"]
    args += [diff_range] if diff_range else ["--cached"]
    return "docs/LIMITATIONS.md" in git(*args).split()


def measure(n=40):
    """
    Precision check before this is ever allowed to block. Runs the diff arm over
    the last N commits and reports how often it fires, so a human can judge
    whether the hits are real claims or noise.
    """
    shas = git("log", "--format=%H", f"-{n}").split()
    fired, total_hits, samples = 0, 0, []
    for sha in shas:
        hits = added_claims(f"{sha}~1..{sha}")
        if hits:
            fired += 1
            total_hits += len(hits)
            if len(samples) < 12:
                subj = git("log", "-1", "--format=%s", sha).strip()
                samples.append((sha[:8], subj[:44], hits[0][0], hits[0][1][:88]))
    print(f"Diff arm over the last {len(shas)} commits")
    print(f"  commits that would have fired : {fired}/{len(shas)}")
    print(f"  total flagged lines           : {total_hits}")
    print()
    print("Sample hits — judge these by hand. A real hit is a sentence that")
    print("states method doctrine without naming what backs it.")
    print()
    for sha, subj, path, text in samples:
        print(f"  {sha}  {subj}")
        print(f"    {path}")
        print(f"    {text}")
    print()
    print("This gate stays WARN-only until these read as mostly-real. A noisy")
    print("gate trains people to ignore it, which is worse than no gate.")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--range", help="git range (default: staged changes)")
    ap.add_argument("--strict", action="store_true", help="exit non-zero on findings")
    ap.add_argument("--measure", action="store_true", help="report precision over recent history")
    args = ap.parse_args()

    if args.measure:
        return measure()

    rows, errors = parse_table()
    problems = list(errors)

    claims = added_claims(args.range)
    if claims and not table_touched(args.range):
        problems.append(
            f"{len(claims)} normative claim(s) added without touching the provenance table:")
        for path, text in claims[:10]:
            problems.append(f"    {path}: {text[:100]}")
        problems.append(
            "  Add a row to the table in docs/LIMITATIONS.md, or name the claim's\n"
            "  standing inline (\"asserted\", \"not measured\", \"single-study\").")

    if not problems:
        counts = {}
        for r in rows:
            counts[r["status"]] = counts.get(r["status"], 0) + 1
        summary = ", ".join(f"{v} {k}" for k, v in sorted(counts.items()))
        print(f"provenance-lint: ok — {len(rows)} claims on record ({summary})")
        return 0

    print("provenance-lint:")
    for p in problems:
        print(f"  {p}")
    print()
    print("  WARN-only. Docs are still committable; the point is that a claim and")
    print("  its standing arrive together, so neither can be mistaken for the other.")
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
