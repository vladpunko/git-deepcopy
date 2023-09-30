# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import logging
import os
import pickle

import pytest

from git_mirrors import api, repository


@pytest.fixture
def cache_path(tmp_path):
    return tmp_path / ".git_mirrors.pickle"


@pytest.fixture
def repositories():
    return [
        "https://github.com/vladpunko/git-mirrors",
        "https://github.com/vladpunko/git-mirrors",  # check for duplicates
    ]


@pytest.fixture
def storage_path(tmp_path):
    return tmp_path / ".repository_mirrors"


def test_mirror(cache_path, repositories, storage_path):
    test_repository = repository.Repository.from_url(parent_path=storage_path, url=repositories[0])

    api.mirror(repositories, storage_path, cache_path)  # run the mirror process

    assert test_repository.local_path.is_dir()
    assert test_repository in pickle.loads(cache_path.read_bytes())
    assert os.listdir(storage_path) == [test_repository.local_path.name]


def test_mirror_no_remote_repository(caplog, cache_path, storage_path):
    test_repository = repository.Repository.from_url(
        parent_path=storage_path, url="https://google.com"
    )

    with caplog.at_level(logging.WARNING):
        api.mirror([test_repository.url], storage_path, cache_path)

    message = f"The remote repository could not be detected for: {test_repository.url!r}."
    assert message in caplog.text


def test_mirror_corrupted_repository(caplog, cache_path, repositories, storage_path):
    test_repository = repository.Repository.from_url(parent_path=storage_path, url=repositories[0])

    api.mirror(repositories, storage_path, cache_path)  # run the mirror process

    (test_repository.local_path / "FETCH_HEAD").unlink()
    with caplog.at_level(logging.WARNING):
        api.mirror(repositories, storage_path, cache_path)  # re-run the mirror process

    message = f"The {str(test_repository.local_path)!r} repository is corrupted."
    assert message in caplog.text


def test_mirror_directory_exists(cache_path, repositories, storage_path):
    repository_path = storage_path / "git-mirrors.git"
    repository_path.mkdir(parents=True)

    api.mirror(repositories, storage_path, cache_path)

    assert repository_path.is_dir()
