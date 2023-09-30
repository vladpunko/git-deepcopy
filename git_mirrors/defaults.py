# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import pathlib
import typing

__all__ = ["CACHE_PATH", "LOGGING_PATH", "SETTINGS_PATH", "STORAGE_PATH"]

_HOME: typing.Final[pathlib.Path] = pathlib.Path.home()

CACHE_PATH: typing.Final[pathlib.Path] = _HOME / ".git_mirrors.pickle"
LOGGING_PATH: typing.Final[pathlib.Path] = _HOME / ".git_mirrors.log"
SETTINGS_PATH: typing.Final[pathlib.Path] = _HOME / ".git_mirrors.json"
# ---
STORAGE_PATH: typing.Final[pathlib.Path] = _HOME / ".repository_mirrors"
