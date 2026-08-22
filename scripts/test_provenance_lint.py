#!/usr/bin/env python3
"""Tests for provenance_lint. The TABLE arm is deterministic and worth pinning;
the DIFF arm is heuristic, so these only pin its exemption classes."""
import importlib.util, pathlib, sys

spec = importlib.util.spec_from_file_location(
    "pl", pathlib.Path(__file__).with_name("provenance_lint.py"))
pl = importlib.util.module_from_spec(spec); spec.loader.exec_module(pl)


def test_table_parses_and_validates():
    rows, errors = pl.parse_table()
    assert rows, "provenance table parsed to zero rows"
    assert not errors, f"table has errors: {errors}"
    assert all(r["status"] in pl.VALID_STATUS for r in rows)


def test_every_evidence_path_resolves():
    rows, _ = pl.parse_table()
    for r in rows:
        if r["evidence"] != "none":
            assert (pl.REPO / r["evidence"]).exists(), f"missing: {r['evidence']}"


def test_doctrine_is_flagged():
    assert pl.NORMATIVE.search("A debate lane cannot precede a blind lane.")
    assert not pl.EXEMPT.search("A debate lane cannot precede a blind lane.")


def test_self_disclosure_is_not_flagged():
    for line in [
        "this method has never been checked against real users",
        "the recall defaults are asserted, not measured",
        "nothing has been calibrated against how humans reacted",
    ]:
        assert pl.INLINE_PROVENANCE.search(line), f"disclosure flagged as claim: {line}"


def test_flag_documentation_is_exempt():
    for line in [
        "- `--version` is required to open a run.",
        "`persona run close` must be called before the report renders.",
    ]:
        assert pl.EXEMPT.search(line), f"CLI docs treated as doctrine: {line}"


if __name__ == "__main__":
    fails = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_"):
            try:
                fn(); print(f"ok   {name}")
            except AssertionError as e:
                fails += 1; print(f"FAIL {name}: {e}")
    sys.exit(1 if fails else 0)
