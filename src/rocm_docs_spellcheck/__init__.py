"""Spellchecking for ROCm documentation."""

from rocm_docs_spellcheck.__version__ import __version__
from rocm_docs_spellcheck.cli import app

__all__ = ["app", "get_version", "__version__"]

if __name__ == "__main__":
    app()
