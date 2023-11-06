from __future__ import annotations

from typing import Any, ClassVar, NamedTuple

from collections.abc import Generator

class Results(
    NamedTuple(
        "Results",
        [
            ("words", list[str]),
            ("context", str),
            ("category", str),
            ("error", str | None),
        ],
    )
):
    def __new__(
        cls,
        words: list[str],
        context: str,
        category: str,
        error: str | None = ...,
    ) -> Results: ...

class SpellChecker:
    DICTIONARY: ClassVar[str]
    GLOB_FLAG_MAP: ClassVar[dict[str, int]]

    binary: str
    verbose: int
    dict_bin: str
    debug: bool
    default_encoding: str

    def __init__(
        self,
        config: dict[str, Any],
        binary: str = ...,
        verbose: int = ...,
        debug: bool = ...,
    ) -> None: ...
    def log(self, text: str, level: int) -> None: ...
    def get_error(self, e: Any) -> str: ...
    def setup_command(
        self,
        encoding: str,
        options: dict[str, Any],
        personal_dict: str | None,
        file_name: str | None = ...,
    ) -> list[str]: ...
    def spell_check_no_pipeline(
        self,
        sources: list[str],
        options: dict[str, Any],
        personal_dict: str | None,
    ) -> Generator[Results, None, None]: ...
    def compile_dictionary(
        self, lang: str, wordlists: list[str], output: str
    ) -> None: ...
    def setup_spellchecker(self, task: dict[str, Any]) -> dict[str, Any]: ...
    def setup_dictionary(self, task: dict[str, Any]) -> str | None: ...
    def run_task(
        self, task: dict[str, Any], source_patterns: list[str] | None = ...
    ) -> Generator[Results, None, None]: ...

class Aspell(SpellChecker): ...
class Hunspell(SpellChecker): ...

def spellcheck(
    config_file: str,
    names: list[str] | None = ...,
    groups: list[str] | None = ...,
    binary: str = ...,
    checker: str = ...,
    sources: list[str] | None = ...,
    verbose: int = ...,
    debug: bool = ...,
) -> Generator[Results, None, None]: ...
