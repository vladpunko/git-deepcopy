# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import hashlib
import io
import logging
import pathlib
import shutil

from git_backupper import exceptions

logger = logging.getLogger(__name__)

__all__ = ["calculate_checksum", "calculate_checksums", "create_directory", "remove_directory"]


def calculate_checksum(path: pathlib.Path, buffer_size: int = io.DEFAULT_BUFFER_SIZE) -> str:
    """Calculate the checksum value for the provided path.

    The function uses the sha-256 algorithm to calculate the hash value. This hash
    function is well-suited for detecting accidental or intentional data changes
    in digital information.
    """
    hash_func = hashlib.sha256()

    try:
        with path.expanduser().open(mode="rb", buffering=0) as stream_in:
            for chunk in iter(lambda: stream_in.read(buffer_size), b""):
                hash_func.update(chunk)
    except OSError as err:
        logger.error("It is impossible to calculate the checksum value for the provided path.")
        raise exceptions.FileSystemError(
            f"Failed to calculate the checksum value for the provided path {str(path)!r}."
        ) from err

    return hash_func.hexdigest()


def calculate_checksums(path: pathlib.Path) -> dict[pathlib.Path, str]:
    """Calculate the checksums of all files in the provided directory path and its
    associated subdirectories on the current working machine.
    """
    checksums: dict[pathlib.Path, str] = {}

    for item in path.glob("**/*"):
        if not item.is_file():
            continue

        checksums[item] = calculate_checksum(item)

    return checksums


def create_directory(path: pathlib.Path) -> None:
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as err:
        logger.error(
            "It is not possible to create a new empty directory on the current computer system."
        )
        raise exceptions.FileSystemError(
            f"Failed to create a new directory at {str(path)!r}."
        ) from err


def remove_directory(path: pathlib.Path) -> None:
    try:
        # There are no built-in python functions to remove a symbolic link to a directory.
        if path.is_symlink():
            path.unlink()
        else:
            shutil.rmtree(path)
    except OSError as err:
        logger.error("It is impossible to remove a directory from the current machine.")
        raise exceptions.FileSystemError(
            f"Failed to remove directory {str(path)!r} from the current working machine."
        ) from err
