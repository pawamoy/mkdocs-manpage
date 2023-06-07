"""Configuration options for the MkDocs Manpage plugin."""

from __future__ import annotations

from mkdocs.config import config_options as mkconf
from mkdocs.config.base import Config as BaseConfig


class PluginConfig(BaseConfig):
    """Configuration options for the plugin."""

    enabled = mkconf.Type(bool, default=True)
    pages = mkconf.ListOfItems(mkconf.Type(str))
    preprocess = mkconf.File(exists=True)
