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
    if tag.name == "a" and ("headerlink" in tag.get("class", "") or tag.img and to_remove(tag.img)):
        return True
    return False


def preprocess(soup: Soup) -> None:
    """Pre-process the soup by removing elements.

    Parameters:
        soup: The soup to modify.
    """
    for element in soup.find_all(to_remove):
        element.decompose()
