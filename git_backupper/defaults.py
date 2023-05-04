# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import pathlib
import typing

__all__ = ["BACKUP_DIRECTORY_PATH", "CACHE_PATH", "SETTINGS_PATH"]

_HOME: typing.Final[pathlib.Path] = pathlib.Path.home()

BACKUP_DIRECTORY_PATH: typing.Final[pathlib.Path] = _HOME / ".backup_repositories"

CACHE_PATH: typing.Final[pathlib.Path] = _HOME / ".git_backupper.pickle"
SETTINGS_PATH: typing.Final[pathlib.Path] = _HOME / ".git_backupper.json"
