# SPDX-License-Identifier: ISC
#
# ISC License
#
# Copyright (c) 2023, Timothée Mazzucotelli and contributors
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""Tests for the plugin."""

from pathlib import Path

import pytest
from duty.tools import mkdocs


def test_plugin(tmp_path: Path) -> None:
    """Generate a manual page from a small MkDocs project."""
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "index.md").write_text("# Test Page\n\nHello from MkDocs.\n", encoding="utf-8")

    config_file = tmp_path / "mkdocs.yml"
    config_file.write_text(
        "site_name: Test Project\n"
        "plugins:\n"
        "  - manpage:\n"
        "      pages:\n"
        "        - output: manpage.1\n"
        "          inputs:\n"
        "            - index.md\n",
        encoding="utf-8",
    )

    with pytest.raises(expected_exception=SystemExit) as exc:
        mkdocs.build(config_file=str(config_file))()

    assert exc.value.code == 0
    assert (tmp_path / "manpage.1").is_file()
    assert "Hello from MkDocs" in (tmp_path / "manpage.1").read_text(encoding="utf-8")
