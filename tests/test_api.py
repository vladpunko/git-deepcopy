# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import logging
import os
import pickle

import pytest

from git_backupper import api, repository


@pytest.fixture
def cache_path(tmp_path):
    return tmp_path / ".git_backupper.pickle"


@pytest.fixture
def backup_path(tmp_path):
    return tmp_path / ".backup_repositories"


@pytest.fixture
def repositories():
    return [
        "https://github.com/vladpunko/git-backupper",
        "https://github.com/vladpunko/git-backupper",  # check for duplicates
    ]


def test_backup(backup_path, cache_path, repositories):
    test_repository = repository.Repository.from_url(parent_path=backup_path, url=repositories[0])

    api.backup(backup_path, repositories, cache_path)  # run the backup process

    assert test_repository.local_path.is_dir()
    assert test_repository in pickle.loads(cache_path.read_bytes())
    assert os.listdir(backup_path) == [test_repository.local_path.name]


def test_backup_no_remote_repository(caplog, backup_path, cache_path):
    test_repository = repository.Repository.from_url(
        parent_path=backup_path, url="https://google.com"
    )

    with caplog.at_level(logging.WARNING):
        api.backup(backup_path, [test_repository.url], cache_path)

    message = f"The remote repository could not be detected for: {test_repository.url!r}."
    assert message in caplog.text


def test_backup_corrupted_repository(caplog, backup_path, cache_path, repositories):
    test_repository = repository.Repository.from_url(parent_path=backup_path, url=repositories[0])

    api.backup(backup_path, repositories, cache_path)  # run the backup process

    (test_repository.local_path / "FETCH_HEAD").unlink()
    with caplog.at_level(logging.WARNING):
        api.backup(backup_path, repositories, cache_path)  # re-run the backup process

    message = f"The {str(test_repository.local_path)!r} repository is corrupted."
    assert message in caplog.text


def test_backup_directory_exists(backup_path, cache_path, repositories):
    repository_path = backup_path / "git-backupper.git"
    repository_path.mkdir(parents=True)

    api.backup(backup_path, repositories, cache_path)

    assert repository_path.is_dir()
