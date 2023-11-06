"""Data from the package."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    # importlib.resources either doesn't exist or lacks the files()
    # function, so use the PyPI version:
    import importlib_resources

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

Traversable: TypeAlias = importlib_resources.abc.Traversable

_PKG_BASE: Traversable = importlib_resources.files(__name__)

WORDLIST: Traversable = _PKG_BASE / "wordlist.txt"


def config_file(name: str) -> Traversable:
    """Get a config file from the package based on name."""
    return _PKG_BASE.joinpath(name + ".yaml")
