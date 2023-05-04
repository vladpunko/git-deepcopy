# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import logging
import reprlib

import pytest

from git_backupper import exceptions, repository


@pytest.fixture
def repository_url():
    return "https://github.com/vladpunko/git-backupper"


def test_repository_class(directory_path, repository_url):
    test_repository = repository.Repository(local_path=directory_path, url=repository_url)

    assert test_repository.local_path == directory_path
    assert test_repository.url == repository_url
    assert str(test_repository) == reprlib.repr(test_repository.to_dict())
    assert repr(test_repository) == (
        f"Repository(local_path={str(directory_path)!r}, url={repository_url!r})"
    )


def test_repository_to_dict(directory_path, repository_url):
    test_repository = repository.Repository(local_path=directory_path, url=repository_url)

    assert test_repository.to_dict() == {"local_path": directory_path, "url": repository_url}


def test_repository_from_url(directory_path, repository_url):
    test_repository = repository.Repository.from_url(parent_path=directory_path, url=repository_url)

    assert test_repository.local_path == directory_path / "git-backupper.git"
    assert test_repository.url == repository_url


def test_repository_create_local_copy(mocker, directory_path, repository_url):
    git_run_command_mock = mocker.patch("git_backupper.repository._run_git_command")

    test_repository = repository.Repository(local_path=directory_path, url=repository_url)
    test_repository.create_local_copy()

    git_run_command_mock.assert_called_once_with(
        repository.GIT_COMMANDS["clone"].format(repository_url, str(directory_path))
    )


def test_repository_update_local_copy(mocker, directory_path, repository_url):
    git_run_command_mock = mocker.patch("git_backupper.repository._run_git_command")

    test_repository = repository.Repository(local_path=directory_path, url=repository_url)
    test_repository.update_local_copy()

    git_run_command_mock.assert_called_once_with(
        repository.GIT_COMMANDS["fetch"].format(str(directory_path))
    )


def test_repository_exists_locally(mocker, directory_path, repository_url):
    git_run_command_mock = mocker.patch("git_backupper.repository._run_git_command")

    test_repository = repository.Repository(local_path=directory_path, url=repository_url)
    test_repository.exists_locally()

    git_run_command_mock.assert_called_once_with(
        repository.GIT_COMMANDS["rev-parse"].format(str(directory_path)), silent=True
    )


def test_repository_not_exists_locally(directory_path, repository_url):
    test_repository = repository.Repository(local_path=directory_path, url=repository_url)

    assert not test_repository.exists_locally()  # directory exists but not a git repository
    directory_path.rmdir()
    assert not test_repository.exists_locally()


def test_repository_exists_on_remote(mocker, directory_path, repository_url):
    git_run_command_mock = mocker.patch("git_backupper.repository._run_git_command")

    test_repository = repository.Repository(local_path=directory_path, url=repository_url)
    test_repository.exists_on_remote()

    git_run_command_mock.assert_called_once_with(
        repository.GIT_COMMANDS["ls-remote"].format(repository_url), silent=True
    )


def test_repository_not_exists_on_remote(directory_path):
    test_repository = repository.Repository(local_path=directory_path, url="https://google.com")

    assert not test_repository.exists_on_remote()


def test_repository_update_local_copy_with_error(caplog, directory_path, repository_url):
    test_repository = repository.Repository(local_path=directory_path, url=repository_url)

    directory_path.rmdir()
    with caplog.at_level(logging.ERROR):
        with pytest.raises(exceptions.ExternalProcessError) as error:
            test_repository.update_local_copy()

    message = "An error occurred on the machine while attempting to execute the command."
    assert message in caplog.text
    assert str(error.value) == (
        "Failed to run the command: {0!r}.".format(
            repository.GIT_COMMANDS["fetch"].format(str(directory_path))
        )
    )
