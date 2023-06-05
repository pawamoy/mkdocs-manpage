"""Configuration options for the MkDocs Manpage plugin."""

from __future__ import annotations

import contextlib
from typing import Any, Dict, Generic, TypeVar

from mkdocs.config import config_options as mkconf
from mkdocs.config.base import Config
from mkdocs.config.base import Config as BaseConfig
from mkdocs.config.config_options import BaseConfigOption, LegacyConfig, ValidationError

T = TypeVar("T")


# TODO: remove once https://github.com/mkdocs/mkdocs/pull/3242 is merged and released
class DictOfItems(Generic[T], BaseConfigOption[Dict[str, T]]):
    """Validates a dict of items. Keys are always strings.

    E.g. for `config_options.DictOfItems(config_options.Type(int))` a valid item is `{"a": 1, "b": 2}`.
    """

    required: bool | None = None  # Only for subclasses to set.

    def __init__(self, option_type: BaseConfigOption[T], default: Any = None) -> None:  # noqa: D107
        super().__init__()
        self.default = default
        self.option_type = option_type
        self.option_type.warnings = self.warnings

    def __repr__(self) -> str:
        return f"{type(self).__name__}: {self.option_type}"

    def pre_validation(self, config: Config, key_name: str) -> None:  # noqa: D102
        self._config = config
        self._key_name = key_name

    def run_validation(self, value: object) -> dict[str, T]:  # noqa: D102
        if value is None:
            if self.required or self.default is None:
                raise ValidationError("Required configuration not provided.")
            value = self.default
        if not isinstance(value, dict):
            raise ValidationError(f"Expected a dict of items, but a {type(value)} was given.")
        if not value:  # Optimization for empty list
            return value

        fake_config = LegacyConfig(())
        with contextlib.suppress(AttributeError):
            fake_config.config_file_path = self._config.config_file_path

        # Emulate a config-like environment for pre_validation and post_validation.
        fake_config.data = value

        for key_name in fake_config:
            self.option_type.pre_validation(fake_config, key_name)
        for key_name in fake_config:
            # Specifically not running `validate` to avoid the OptionallyRequired effect.
            fake_config[key_name] = self.option_type.run_validation(fake_config[key_name])
        for key_name in fake_config:
            self.option_type.post_validation(fake_config, key_name)

        return value


class PluginConfig(BaseConfig):
    """Configuration options for the plugin."""

    enabled = mkconf.Type(bool, default=True)
    pages = mkconf.ListOfItems(mkconf.Type(str))
