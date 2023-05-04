# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import abc
import collections.abc
import pathlib
import typing

from git_backupper import exceptions

__all__ = ["PathField", "SequenceField"]

_T = typing.TypeVar("_T")
_V = typing.TypeVar("_V")


class _Field(abc.ABC, typing.Generic[_V, _T]):
    def __set_name__(self, owner: type[typing.Any], name: str) -> None:
        self.name = name

    def __get__(self, instance: typing.Any, owner: type[typing.Any]) -> _T:
        if instance is None:
            return self  # type: ignore

        return typing.cast(_T, instance.__dict__[self.name])

    def __set__(self, instance: typing.Any, value: _V) -> None:
        instance.__dict__[self.name] = self.process_value(value)

    @abc.abstractmethod
    def process_value(self, value: _V) -> _T:
        """Validate and normalize the value of the field and return it if valid."""
        raise NotImplementedError


class PathField(_Field[typing.Union[str, pathlib.Path], pathlib.Path]):
    def process_value(self, value: typing.Union[str, pathlib.Path]) -> pathlib.Path:
        if not isinstance(value, (str, pathlib.Path)):
            raise exceptions.SettingsError(
                f"Path must be string, but received: {type(value).__name__}."
            )

        if not value:
            raise exceptions.SettingsError("Path can not be empty.")

        return pathlib.Path(value).expanduser()


class SequenceField(_Field[typing.Iterable[str], list[str]]):
    def process_value(self, value: typing.Iterable[str]) -> list[str]:
        if not isinstance(value, collections.abc.Sequence) or isinstance(value, (bytes, str)):
            raise exceptions.SettingsError(
                "The data required for a list field must be inputted as a sequence or array."
            )

        if not all(isinstance(item, str) for item in value):
            raise exceptions.SettingsError("All items in sequence must be strings.")

        return sorted(set(value))  # remove all duplicates
