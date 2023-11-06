"""Defines reporters for the spell check results."""

from __future__ import annotations

from typing import ClassVar, NamedTuple

import sys
from abc import ABC, abstractmethod
from enum import Enum

from rich.align import Align
from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel
from rich.theme import Theme

from pyspelling import Results

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override


class Options(NamedTuple):
    """Common options for reporters."""

    print_category: bool


class Base(ABC):
    """Base class for reporters."""

    def __init__(self, options: Options) -> None:
        """Create the reporter."""
        self._options = options

    @abstractmethod
    def report(self, results: Results) -> None:
        """Report a single result."""

    def summarize(self) -> bool | None:
        """Called after all results have been reported. Return false to fail the script."""


class RichConsoleReporter(Base):
    """Formats results using rich and reports to the console."""

    _THEME: ClassVar[Theme] = Theme(
        {
            "error": "red",
            "highlight": "yellow",
            "info": "blue",
            "str": "green",
            "success": "bold green",
        }
    )
    _ERR_CONSOLE = Console(theme=_THEME, stderr=True)

    @override
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        self._fail = False

    @override
    def report(self, results: Results) -> None:
        if results.error:
            self._fail = True
            self._ERR_CONSOLE.print(
                Panel(
                    results.error,
                    title=f"[bold]Error[/bold]: {results.context}",
                    border_style="error",
                )
            )
        elif results.words:
            self._fail = True
            group = Group(
                Align.center(
                    Panel(
                        f"[info][bold]Context[/bold][/info]: [str]{results.context}[/str]"
                        f" [info][bold]Category[/bold][/info]: [str]{results.category}[/str]",
                        expand=False,
                        border_style="info",
                    )
                )
                if self._options.print_category
                else "",
                Columns(f"[highlight]{w}[/highlight]" for w in results.words),
            )
            panel = Panel(
                group,
                title="[bold]Mispelled words"
                + (
                    "[/bold]"
                    if self._options.print_category
                    else f" in[/bold] [str]{results.context}[/str]"
                ),
                border_style="error",
            )
            self._ERR_CONSOLE.print(panel)

    @override
    def summarize(self) -> bool:
        if self._fail:
            return False
        self._ERR_CONSOLE.print("[success]Spelling check passed.[/success]")
        return True


class CollectReporter(Base):
    """Collects all mispelled words."""

    @override
    def __init__(self, options: Options) -> None:
        super().__init__(options)
        self._words: set[str] = set()

    @override
    def report(self, results: Results) -> None:
        if results.error:
            return
        if not results.words:
            return
        self._words.update(results.words)

    @override
    def summarize(self) -> None:
        for word in sorted(self._words):
            print(word)


class Type(str, Enum):
    """Reporter Type"""

    console = ("console",)
    collect = "collect"


_REPORTERS: dict[Type, type[Base]] = {
    Type.console: RichConsoleReporter,
    Type.collect: CollectReporter,
}


def create(type: Type, options: Options) -> Base:
    """Create a reporter based on the type."""
    return _REPORTERS[type](options)
