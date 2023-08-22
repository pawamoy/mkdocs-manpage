"""MkDocs plugin that generates a manpage at the end of the build."""

from __future__ import annotations

import subprocess
import tempfile
from datetime import date
from importlib import metadata
from pathlib import Path
from shutil import which
from typing import TYPE_CHECKING

from mkdocs.plugins import BasePlugin

from mkdocs_manpage.config import PluginConfig
from mkdocs_manpage.logger import get_logger
from mkdocs_manpage.preprocess import preprocess

if TYPE_CHECKING:
    from typing import Any

    from mkdocs.config.defaults import MkDocsConfig
    from mkdocs.structure.pages import Page


logger = get_logger(__name__)


def _log_pandoc_output(output: str) -> None:
    for line in output.split("\n"):
        if line.strip():
            logger.debug(f"pandoc: {line.strip()}")


class MkdocsManpagePlugin(BasePlugin[PluginConfig]):
    """The MkDocs plugin to generate manpages.

    This plugin defines the following event hooks:

    - `on_page_content`
    - `on_post_build`

    Check the [Developing Plugins](https://www.mkdocs.org/user-guide/plugins/#developing-plugins) page of `mkdocs`
    for more information about its plugin system.
    """

    mkdocs_config: MkDocsConfig

    def __init__(self) -> None:  # noqa: D107
        self.pages: dict[str, str] = {}

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        """Save the global MkDocs configuration.

        Hook for the [`on_config` event](https://www.mkdocs.org/user-guide/plugins/#on_config).
        In this hook, we save the global MkDocs configuration into an instance variable,
        to re-use it later.

        Arguments:
            config: The MkDocs config object.

        Returns:
            The same, untouched config.
        """
        self.mkdocs_config = config
        return config

    def on_page_content(self, html: str, *, page: Page, **kwargs: Any) -> str | None:  # noqa: ARG002
        """Record pages contents.

        Hook for the [`on_page_content` event](https://www.mkdocs.org/user-guide/plugins/#on_page_content).
        In this hook we simply record the HTML of the pages into a dictionary whose keys are the pages' URIs.

        Parameters:
            html: The page HTML.
            page: The page object.
        """
        if not self.config.enabled:
            return None
        if page.file.src_uri in self.config.pages or not self.config.pages:
            logger.debug(f"Adding page {page.file.src_uri} to manpage")
            self.pages[page.file.src_uri] = html
        return html

    def on_post_build(self, config: MkDocsConfig, **kwargs: Any) -> None:  # noqa: ARG002
        """Combine all recorded pages contents and convert it to a manual page with Pandoc.

        Hook for the [`on_post_build` event](https://www.mkdocs.org/user-guide/plugins/#on_post_build).
        In this hook we concatenate all previously recorded HTML, and convert it to a manual page with Pandoc.

        Parameters:
            config: MkDocs configuration.
        """
        if not self.config.enabled:
            return
        pandoc = which("pandoc")
        if pandoc is None:
            logger.debug("Could not find pandoc executable, trying to call 'pandoc' directly")
            pandoc = "pandoc"
        pages = []
        if self.config.pages:
            for page in self.config.pages:
                try:
                    pages.append(self.pages[page])
                except KeyError:
                    logger.error(f"No page with path {page}")  # noqa: TRY400
        else:
            pages = list(self.pages.values())
        html = "\n\n".join(pages)

        if self.config.preprocess:
            html = preprocess(html, self.config.preprocess)

        output_file = Path(config.site_dir, "manpage.1")
        with tempfile.NamedTemporaryFile("w", prefix="mkdocs_manpage_", suffix=".1.html") as temp_file:
            temp_file.write(html)
            pandoc_variables = [
                f"title:{self.mkdocs_config.site_name}",
                "section:1",
                f"date:{date.today().strftime('%Y-%m-%d')}",  # noqa: DTZ011
                f"footer:mkdocs-manpage v{metadata.version('mkdocs-manpage')}",
                "header:User Commands",
            ]
            pandoc_options = [
                "--verbose",
                "--standalone",
                "--wrap=none",
            ]
            pandoc_command = [
                pandoc,
                *pandoc_options,
                *[f"-V{var}" for var in pandoc_variables],
                "--to",
                "man",
                temp_file.name,
                "-o",
                str(output_file),
            ]
            pandoc_process = subprocess.run(
                pandoc_command,  # noqa: S603
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )
        _log_pandoc_output(pandoc_process.stdout)
        logger.info(f"Generated manpage at {output_file}")
