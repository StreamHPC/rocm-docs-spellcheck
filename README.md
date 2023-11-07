# Spell check tool for ROCm documentation

## Purpose

This repository hosts a command line tool `rocm-docs-spellcheck` to check for
spelling mistakes in documentation files. It supplies the common word-list used
in ROCm documentation, and defines a [`pre-commit`](https://pre-commit.com/) hook
that checks for spelling mistakes.

## Usage

### As a `pre-commit` hook

The recommended usage is as a `pre-commit` hook. Install `pre-commit` and add the
following to `.pre-commit-config.yaml` in your repository root:

```yaml
- repo: https://github.com/StreamHPC/rocm-docs-spellcheck
  rev: v0.1.0
  hooks:
  - id: spellcheck-markdown
  - id: mispelled-markdown # For collecting all mispelled words
```

For more options and information you can refer to
[Adding pre-commit plugins to your project](https://pre-commit.com/#plugins).

### Print all mispelled words

The hooks `mispelled-<language>` can be used to collect all mispelled words
from all files, this can be useful for adding missing words to the word-list,
after the legitimate mispellings have been fixed.
Use it by running `pre-commit run --verbose --hook-stage=manual mispelled-markdown`

## Development Notes

The tool is a wrapper around [`pyspelling`](https://facelessuser.github.io/pyspelling/)
to make it more suitable as a `pre-commit` hook.
The most important changes compared to `pyspelling` are:
- the files to check must be explicitly passed, because `pre-commit` contains
  its own logic for which files to check
- the repository bundles configurations for checking `myst`-enabled markdown files.
- the task (an element in the matrix part of `pyspelling` configuration) must
  also be explicitly passed on the command line, because `pyspelling` only
  allows a single task to be active when an explicit list of sources is passed.
- a word-list is bundled with this repository and its automatically added to
  the configuration
- the dictionary output is saved to a temporary file instead of `dictionary.dic`
  by default.
