"""
Milestone 1 sanity test.

This doesn't test any real feature yet — it tests that the *packaging*
itself works: that `basewise` is importable and that its version is
readable. This will catch mistakes like forgetting to register a new
subpackage, or a typo breaking the import chain, before we build
anything real on top of it.
"""

import basewise


def test_version_exists():
    assert basewise.__version__ == "0.1.0"


def test_version_is_string():
    assert isinstance(basewise.__version__, str)
