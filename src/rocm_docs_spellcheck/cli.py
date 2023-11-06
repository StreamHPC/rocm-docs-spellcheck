"""Defines the command line interface for the package."""

from typing import Any, List, Union

import sys
from pathlib import Path

import typer
import yaml

import pyspelling
import pyspelling.util
import rocm_docs_spellcheck.reporters as reporters
from rocm_docs_spellcheck import data
from rocm_docs_spellcheck.__version__ import __version__

if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if not value:
        return
    print(__version__)
    raise typer.Exit()


@app.command()
def cli(
    name: Annotated[str, typer.Option()],
    filenames: List[Path],
    verbose: Annotated[List[bool], typer.Option("--verbose", "-v")] = [],
    user_wordlist: Annotated[
        List[Path],
        typer.Option(
            "--wordlist",
            "-w",
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
        ),
    ] = [],
    reporter_type: Annotated[
        reporters.Type, typer.Option("--reporter")
    ] = reporters.Type.console,
    print_category: bool = False,
    _: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Print the version and exit the program",
            callback=_version_callback,
            is_eager=True,
        ),
    ] = False,
) -> None:
    """Spellcheck the files based on a predefined setting."""
    reporter = reporters.create(
        reporter_type, reporters.Options(print_category)
    )

    config_file = data.config_file(name)
    wordlists: List[Union[data.Traversable, Path]] = [
        data.WORDLIST,
        *user_wordlist,
    ]

    # Pyspelling leaves no option but to do this.
    # We want to change the wordlist dynamically, but not write out the whole config to a temporary
    # file.
    # We have to match the parameter name even if we don't use it.
    def patched_read_config(file_name: str) -> Any:  # noqa: ARG001
        config = yaml.safe_load(config_file.open())
        config.setdefault("dictionary", {})["wordlists"] = wordlists
        config["name"] = name
        return {"matrix": [config]}

    pyspelling.util.read_config = patched_read_config

    for results in pyspelling.spellcheck(
        "",
        names=[name],
        sources=[str(f) for f in filenames],
        verbose=len(verbose),
    ):
        reporter.report(results)

    final_result = reporter.summarize()
    if final_result is not None and final_result is False:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
