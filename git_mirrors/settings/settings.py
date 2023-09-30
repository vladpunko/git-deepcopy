# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import json
import logging
import pathlib
import typing

from git_mirrors import defaults, exceptions
from git_mirrors.settings import fields

logger = logging.getLogger("git_mirrors")

__all__ = ["Settings"]

_T = typing.TypeVar("_T", bound="Settings")


class Settings:
    # schema
    repositories = fields.SequenceField()  # List[str]
    storage_path = fields.PathField()  # Path

    def __init__(
        self,
        repositories: typing.List[str],
        storage_path: typing.Union[str, pathlib.Path] = defaults.STORAGE_PATH,
    ) -> None:
        self.repositories = repositories
        self.storage_path = storage_path

    @classmethod
    def from_json(
        cls: typing.Type[_T],
        path: typing.Union[str, pathlib.Path] = defaults.SETTINGS_PATH,
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
        if not {"repositories"} <= set(settings.keys()) <= {"storage_path", "repositories"}:
            raise exceptions.SettingsError("File does not match expected schema.")

        return cls(**settings)

    def __str__(self) -> str:
        return json.dumps(self.to_dict(), default=str, indent=2)  # serialize

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(repositories={self.repositories}, storage_path={str(self.storage_path)!r})"
        )

    def to_dict(self) -> typing.Dict[str, typing.Union[pathlib.Path, typing.List[str]]]:
        return self.__dict__
