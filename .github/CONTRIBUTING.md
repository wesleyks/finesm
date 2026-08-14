# Contributing

## Prerequisites

- Python 3.11 or later.
- Poetry 2.4.

## Setup and validation

Install the locked development environment with:

```sh
poetry sync
```

Before opening a pull request, run:

```sh
poetry check --lock
poetry run pytest
poetry build
```

## Maintainer releases

Use a Conventional Commit-style pull request title, such as `fix: ...`,
`feat: ...`, or `feat!: ...`, when squash-merging changes. See [the release
runbook](../docs/RELEASING.md) for the automated Release Please and PyPI
publishing process.

