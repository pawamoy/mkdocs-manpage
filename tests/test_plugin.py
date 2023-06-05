"""Tests for the plugin."""

import os

import pytest
from duty.callables import mkdocs


def test_plugin() -> None:
    """Run the plugin."""
    os.environ["MANPAGE"] = "true"
    with pytest.raises(expected_exception=SystemExit) as exc:
        mkdocs.build()()
    assert exc.value.code == 0
