# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import logging
import os

import pytest

from git_backupper import exceptions, fs


def test_create_directory(directory_path):
    path = directory_path / "directory"
    fs.create_directory(path)
    assert path.is_dir()


def test_create_directory_with_error(caplog, directory_path):
    os.chmod(directory_path, 0o000)
    path = directory_path / "directory"

    with caplog.at_level(logging.ERROR):
        with pytest.raises(exceptions.FileSystemError) as error:
            fs.create_directory(path)

    message = "It is not possible to create a new empty directory on the current computer system."
    assert message in caplog.text
    assert str(error.value) == f"Failed to create a new directory at {str(path)!r}."


def test_remove_directory(directory_path):
    fs.remove_directory(directory_path)
    assert not directory_path.is_dir()


def test_remove_directory_in_case_symlink(symlink_path):
    fs.remove_directory(symlink_path)
    assert not symlink_path.exists()


def test_remove_directory_with_error(caplog, directory_path):
    os.chmod(directory_path, 0o000)

    with caplog.at_level(logging.ERROR):
        with pytest.raises(exceptions.FileSystemError) as error:
            fs.remove_directory(directory_path)

    message = "It is impossible to remove a directory from the current machine."
    assert message in caplog.text
    assert str(error.value) == (
        f"Failed to remove directory {str(directory_path)!r} from the current working machine."
    )


def test_calculate_checksum(checksums):
    for path, checksum in checksums.items():
        assert fs.calculate_checksum(path) == checksum


def test_calculate_checksum_with_error(caplog, checksums):
    for path in checksums:
        os.chmod(path, 0o000)

        with caplog.at_level(logging.ERROR):
            with pytest.raises(exceptions.FileSystemError) as error:
                fs.calculate_checksum(path)

        message = "It is impossible to calculate the checksum value for the provided path."
        assert message in caplog.text
        assert str(error.value) == (
            f"Failed to calculate the checksum value for the provided path {str(path)!r}."
        )


def test_calculate_checksums(checksums, directory_path, symlink_path):
    assert fs.calculate_checksums(directory_path) == checksums

    checksums = fs.calculate_checksums(symlink_path)
    assert checksums == {}
