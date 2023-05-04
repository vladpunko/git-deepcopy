# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import json
import logging
import pathlib
import typing

from git_backupper import defaults, exceptions
from git_backupper.settings import fields

logger = logging.getLogger(__name__)

__all__ = ["Settings"]

_T = typing.TypeVar("_T", bound="Settings")


class Settings:
    # schema
    backup_path = fields.PathField()  # Path
    repositories = fields.SequenceField()  # List[str]

    def __init__(
        self,
        repositories: list[str],
        backup_path: typing.Union[str, pathlib.Path] = defaults.BACKUP_DIRECTORY_PATH,
    ) -> None:
        self.backup_path = backup_path
        self.repositories = repositories

    @classmethod
    def from_json(
        cls: type[_T], path: typing.Union[str, pathlib.Path] = defaults.SETTINGS_PATH
    ) -> _T:
        try:
            with pathlib.Path(path).expanduser().open(encoding="utf-8") as stream_in:
                settings = json.load(stream_in)
        except OSError as err:
            logger.error("It is impossible to load the settings from the determined location.")
            raise exceptions.FileSystemError(
                f"Failed to load the settings from the provided path: {str(path)!r}."
            ) from err

        except json.JSONDecodeError as err:
            logger.error("The settings data you are trying to parse may be corrupt or incomplete.")
            raise exceptions.SettingsError(
                f"Failed to parse the settings data from the provided path: {str(path)!r}."
            ) from err

        # Ensure that the settings conform to the expected schema before using them.
        if not {"repositories"} <= set(settings.keys()) <= {"backup_path", "repositories"}:
            raise exceptions.SettingsError("File does not match expected schema.")

        return cls(**settings)

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), default=str, indent=2)  # serialize

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(repositories={self.repositories}, backup_path={str(self.backup_path)!r})"
        )

    def to_dict(self) -> dict[str, typing.Union[pathlib.Path, list[str]]]:
        return self.__dict__
