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

"""HTML pre-processing module."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bs4 import BeautifulSoup as Soup
    from bs4 import Tag


def to_remove(tag: Tag) -> bool:
    """Tell whether a tag should be removed from the soup.

    Parameters:
        tag: The tag to check.

    Returns:
        True or false.
    """
    # Remove images and SVGs.
    if tag.name in {"img", "svg"}:
        return True
    # Remove permalinks.
    return bool(tag.name == "a" and ("headerlink" in (tag.get("class") or "") or (tag.img and to_remove(tag.img))))


def preprocess(soup: Soup, output: str) -> None:  # noqa: ARG001
    """Pre-process the soup by removing elements.

    Parameters:
        soup: The soup to modify.
        output: The manpage output path.
    """
    for element in soup.find_all(to_remove):
        element.decompose()
