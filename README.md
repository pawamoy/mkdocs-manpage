# MkDocs Manpage

[![ci](https://github.com/pawamoy/mkdocs-manpage/workflows/ci/badge.svg)](https://github.com/pawamoy/mkdocs-manpage/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/mkdocs-manpage/)
[![pypi version](https://img.shields.io/pypi/v/mkdocs-manpage.svg)](https://pypi.org/project/mkdocs-manpage/)
[![gitpod](https://img.shields.io/badge/gitpod-workspace-blue.svg?style=flat)](https://gitpod.io/#https://github.com/pawamoy/mkdocs-manpage)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://app.gitter.im/#/room/#mkdocs-manpage:gitter.im)

MkDocs plugin to generate a manpage from the documentation site.

## Requirements

Pandoc must be [installed](https://pandoc.org/installing.html) and available as `pandoc`.

## Installation

With `pip`:

```bash
pip install mkdocs-manpage[preprocess]
```

With [`pipx`](https://github.com/pipxproject/pipx):

```bash
python3.8 -m pip install --user pipx
pipx install mkdocs-manpage[preprocess]
```

## Usage

```yaml
# mkdocs.yml
plugins:
- manpage:
    pages:
    - index.md
    - usage.md
    - reference/api.md
```

To enable/disable the plugin with an environment variable:

```yaml
# mkdocs.yml
plugins:
- manpage:
    enabled: !ENV [MANPAGE, false]
```

Then set the environment variable and run MkDocs:

```bash
MANPAGE=true mkdocs build
```

The manpage will be written into the root of the site directory
and named `manpage.1`.

### Pre-processing HTML

This plugin works by concatenating the HTML from all selected pages
into a single file that is then converted to a manual page using Pandoc.

With a complete conversion, the final manual page will not look so good.
For example images and SVG will be rendered as long strings of data and/or URIs.
So this plugin allows users to pre-process the HTML, to remove unwanted
HTML elements before converting the whole thing to a manpage.

First, you must make sure to install the `preprocess` extra:

```bash
pip install mkdocs-manpage[preprocess]
```

To pre-process the HTML, we use [BeautifulSoup](https://pypi.org/project/beautifulsoup4/).
Users have to write their own `preprocess` function in order to modify the soup
returned by BeautifulSoup:

```python title="scripts/preprocess.py"
from bs4 import BeautifulSoup, Tag


def to_remove(tag: Tag) -> bool:
    # remove images and SVGs
    if tag.name in {"img", "svg"}:
        return True
    # remove links containing images or SVGs
    if tag.name == "a" and tag.img and to_remove(tag.img):
        return True
    # remove permalinks
    if tag.name == "a" and "headerlink" in tag.get("class", ()):
        return True
    return False


def preprocess(soup: BeautifulSoup) -> None:
    for element in soup.find_all(to_remove):
        element.decompose()
```

Then, instruct the plugin to use this module and its `preprocess` function:

```yaml title="mkdocs.yml"
plugins:
- manpage:
    preprocess: scripts/preprocess.py
```

See the documentation of both [`BeautifulSoup`][bs4.BeautifulSoup] and [`Tag`][bs4.Tag]
to know what methods are available to correctly select the elements to remove.

The alternative to HTML processing for improving the final manpage
is disabling some options from other plugins/extensions:

- no source code through `mkdocstrings`:

    ```yaml
    - mkdocstrings:
        handlers:
          python:
            options:
              show_source: !ENV [SHOW_SOURCE, true]
    ```

- no permalink through `toc`:

    ```yaml
    markdown_extensions:
    - toc:
        permalink: !ENV [PERMALINK, true]
    ```

Then set these environment variables before building
the documentation and generating the manpage:

```bash
export MANPAGE=true
export PERMALINK=false
export SHOW_SOURCE=false
mkdocs build
```
