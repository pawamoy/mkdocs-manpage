# MkDocs Manpage

[![ci](https://github.com/pawamoy/mkdocs-manpage/workflows/ci/badge.svg)](https://github.com/pawamoy/mkdocs-manpage/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/mkdocs-manpage/)
[![pypi version](https://img.shields.io/pypi/v/mkdocs-manpage.svg)](https://pypi.org/project/mkdocs-manpage/)
[![gitpod](https://img.shields.io/badge/gitpod-workspace-blue.svg?style=flat)](https://gitpod.io/#https://github.com/pawamoy/mkdocs-manpage)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://gitter.im/mkdocs-manpage/community)

MkDocs plugin to generate a manpage from the documentation site.

## Requirements

Pandoc must be [installed](https://pandoc.org/installing.html) and available as `pandoc`.

## Installation

With `pip`:
```bash
pip install mkdocs-manpage
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python3.7 -m pip install --user pipx
pipx install mkdocs-manpage
```

## Usage

```yaml
# mkdocs.yml
plugins:
- manpage:
    enabled: !ENV [MANPAGE, false]
    pages:
    - index.md
    - usage.md
    - reference/api.md
```

We also recommend disabling some options from other plugins/extensions
to improve the final manual page:

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
# manpage is in site dir: ./site/manpage.1
```
