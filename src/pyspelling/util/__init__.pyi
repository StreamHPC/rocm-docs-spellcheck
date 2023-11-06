from __future__ import annotations

from typing import Any, Callable, TypeVar

import sys

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

import re
import subprocess

import yaml.cyaml
import yaml.loader

RE_LAST_SPACE_IN_CHUNK: re.Pattern[bytes]

Param = ParamSpec("Param")
RetType = TypeVar("RetType")

def deprecated(
    message: str,
) -> Callable[[Callable[Param, RetType]], Callable[Param, RetType]]: ...
def warn_deprecated(message: str) -> None: ...
def get_process(cmd: list[str]) -> subprocess.Popen[str]: ...
def get_process_output(
    process: subprocess.Popen[str], encoding: str | None = ...
) -> str: ...
def call(
    cmd: list[str],
    input_file: str | None = ...,
    input_text: str | None = ...,
    encoding: str | None = ...,
) -> str: ...
def call_spellchecker(
    cmd: list[str], input_text: str | None = ..., encoding: str | None = ...
) -> str: ...
def random_name_gen(size: int = ...) -> str: ...
def yaml_load(
    source: str, loader: type[yaml.loader._Loader | yaml.cyaml._CLoader] = ...
) -> Any: ...
def read_config(file_name: str) -> Any: ...
