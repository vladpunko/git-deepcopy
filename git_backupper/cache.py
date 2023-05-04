# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import collections
import logging
import pathlib
import pickle
import typing

from git_backupper import defaults, exceptions

logger = logging.getLogger(__name__)

__all__ = ["PersistentCache"]


class PersistentCache(collections.UserDict[typing.Hashable, typing.Any]):
    def __init__(self, path: typing.Union[str, pathlib.Path] = defaults.CACHE_PATH) -> None:
        super().__init__()

        self.path = pathlib.Path(path).expanduser()

    def __enter__(self) -> dict[typing.Hashable, typing.Any]:
        if self.path.is_file():
            self._load()

        return self.data

    def __exit__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        self._save()

    def _load(self) -> None:
        try:
            with self.path.open(mode="rb") as stream_in:
                self.update(pickle.load(stream_in))
        except OSError as err:
            logger.error(
                "A sudden issue emerged while trying to load the data from the present device."
            )
            raise exceptions.FileSystemError(
                f"Failed to load data from {str(self.path)!r}."
            ) from err

        except (EOFError, pickle.UnpicklingError) as err:
            logger.error("The attempt to retrieve data stored using pickle has failed.")
            raise exceptions.SettingsError(
                "Unable to convert the input data into its original or structured form."
            ) from err

    def _save(self) -> None:
        try:
            with self.path.open(mode="wb") as stream_out:
                pickle.dump(self.data, stream_out, protocol=pickle.HIGHEST_PROTOCOL)
        except OSError as err:
            logger.error(
                "An error occurred while trying to dump data and save it to the current machine."
            )
            raise exceptions.FileSystemError(f"Failed to dump data to {str(self.path)!r}.") from err
