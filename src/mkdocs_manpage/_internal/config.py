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

from __future__ import annotations

from mkdocs.config import config_options as mkconf
from mkdocs.config.base import Config as BaseConfig


class PageConfig(BaseConfig):
    """Sub-config for each manual page."""

    title = mkconf.Optional(mkconf.Type(str))
    """Title to show in the manual page; defaults to the site name."""

    header = mkconf.Optional(mkconf.Type(str))
    """Header to show in the manual page; defaults to the standard section header."""

    output = mkconf.File(exists=False)
    """Path of the generated manual page, relative to the MkDocs config file."""

    inputs = mkconf.ListOfItems(mkconf.Type(str))
    """Source page URIs to include, with optional `*` patterns."""


class PluginConfig(BaseConfig):
    """Configuration options for the plugin."""

    enabled = mkconf.Type(bool, default=True)
    """Whether to generate manual pages."""

    preprocess = mkconf.Optional(mkconf.File(exists=True))
    """Path to a Python file that preprocesses each manual page's HTML."""

    pages = mkconf.ListOfItems(mkconf.SubConfig(PageConfig))
    """Configuration for the manual pages to generate."""
