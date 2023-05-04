# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import dataclasses
import logging
import os
import pathlib
import reprlib
import shlex
import subprocess
import types
import typing

from git_backupper import exceptions

GIT_COMMANDS: typing.Final[types.MappingProxyType[str, str]] = types.MappingProxyType(
    {
        "clone": "git clone --mirror --no-hardlinks -- {0!r} {1!r}",
        "fetch": "git -C {0!r} fetch --all --verbose",
        "ls-remote": "git ls-remote --exit-code -- {0!r}",
        "rev-parse": "git -C {0!r} rev-parse --git-dir",
    }
)

logger = logging.getLogger(__name__)

__all__ = ["Repository"]

_T = typing.TypeVar("_T", bound="Repository")


def _get_repository_name(url: str) -> str:
    """Return the name of a particular repository specified by its web address."""
    name = url.split("/").pop()

    return name if name.endswith(".git") else f"{name}.git"


def _run_git_command(command: str, silent: bool = False) -> None:
    env: dict[str, str] = {
        # Disables the prompting of the git credential helper and avoids blocking
        # when the user is required to enter authentication credentials.
        "GIT_TERMINAL_PROMPT": "0",
    }
    env.update(os.environ)

    stdout = stderr = subprocess.DEVNULL if silent else None  # streams
    try:
        subprocess.check_call(shlex.split(command), env=env, stdout=stdout, stderr=stderr)
    except subprocess.CalledProcessError as err:
        if not silent:
            logger.error(
                "An error occurred on the machine while attempting to execute the command."
            )
        raise exceptions.ExternalProcessError(f"Failed to run the command: {command!r}.") from err


@dataclasses.dataclass(frozen=True)
class Repository:
    local_path: pathlib.Path
    url: str

    @classmethod
    def from_url(cls: type[_T], url: str, parent_path: pathlib.Path) -> _T:
        """This method allows creating a repository instance knowing only the repository
        storage path on the current working machine.
        """
        return cls(local_path=(parent_path / _get_repository_name(url)).expanduser(), url=url)

    def __str__(self) -> str:
        return reprlib.repr(self.to_dict())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(local_path={str(self.local_path)!r}, url={self.url!r})"

    def create_local_copy(self) -> None:
        # Clone a mirrored copy of the specified repository onto the current machine.
        _run_git_command(GIT_COMMANDS["clone"].format(self.url, str(self.local_path)))

    def exists_locally(self) -> bool:
        if not self.local_path.is_dir():
            return False

        try:
            _run_git_command(GIT_COMMANDS["rev-parse"].format(str(self.local_path)), silent=True)
        except exceptions.ExternalProcessError:
            return False

        return True

    def exists_on_remote(self) -> bool:
        try:
            _run_git_command(GIT_COMMANDS["ls-remote"].format(self.url), silent=True)
        except exceptions.ExternalProcessError:
            return False

        return True

    def to_dict(self) -> dict[str, typing.Union[str, pathlib.Path]]:
        return dataclasses.asdict(self)

    def update_local_copy(self) -> None:
        _run_git_command(GIT_COMMANDS["fetch"].format(str(self.local_path)))
