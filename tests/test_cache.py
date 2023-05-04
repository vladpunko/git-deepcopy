# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import logging
import os
import pickle

import pytest

from git_backupper import cache, exceptions


def test_cache_save(checksums, file_path):
    file_path.unlink()

    with cache.PersistentCache(path=file_path) as test_cache:
        test_cache.update(checksums)

    assert checksums == pickle.loads(file_path.read_bytes())


def test_cache_save_with_error(caplog, checksums, file_path):
    file_path.write_bytes(pickle.dumps(checksums))

    with caplog.at_level(logging.ERROR):
        with pytest.raises(exceptions.FileSystemError) as error:
            with cache.PersistentCache(path=file_path) as test_cache:
                os.chmod(file_path, 0o000)

                test_cache.update(checksums)

    message = "An error occurred while trying to dump data and save it to the current machine."
    assert message in caplog.text
    assert str(error.value) == f"Failed to dump data to {str(file_path)!r}."


def test_cache_load(checksums, file_path):
    file_path.write_bytes(pickle.dumps(checksums))

    with cache.PersistentCache(path=file_path) as test_cache:
        assert checksums == test_cache


def test_cache_load_with_error(caplog, checksums, file_path):
    os.chmod(file_path, 0o000)

    with caplog.at_level(logging.ERROR):
        with pytest.raises(exceptions.FileSystemError) as error:
            with cache.PersistentCache(file_path):
                pass

    message = "A sudden issue emerged while trying to load the data from the present device."
    assert message in caplog.text
    assert str(error.value) == f"Failed to load data from {str(file_path)!r}."


def test_cache_load_with_unpickle_error(caplog, checksums, file_path):
    file_path.write_bytes(b"test")

    with caplog.at_level(logging.ERROR):
        with pytest.raises(exceptions.SettingsError) as error:
            with cache.PersistentCache(path=file_path):
                pass

    message = "The attempt to retrieve data stored using pickle has failed."
    assert message in caplog.text
    assert str(error.value) == (
        "Unable to convert the input data into its original or structured form."
    )
