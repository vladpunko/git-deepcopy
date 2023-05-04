# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import json
import logging
import pathlib

import pytest

from git_backupper import exceptions
from git_backupper.settings import settings


@pytest.fixture
def backup_path():
    path = pathlib.Path("~/directory")

    return path


@pytest.fixture
def repositories():
    return ["1.git", "2.git", "3.git"]


@pytest.fixture
def settings_path(backup_path, repositories, fs):
    path = pathlib.Path("settings.json")
    path.write_text(json.dumps({"backup_path": str(backup_path), "repositories": repositories}))

    return path


@pytest.fixture
def settings_dict(backup_path, repositories):
    return {"backup_path": backup_path.expanduser(), "repositories": repositories}


def test_settings_class(backup_path, repositories, settings_dict):
    test_settings = settings.Settings(repositories=repositories * 5, backup_path=backup_path)

    assert str(test_settings.backup_path) == str(backup_path.expanduser())
    assert test_settings.repositories == repositories
    assert str(test_settings) == json.dumps(settings_dict, default=str, indent=2)
    assert repr(test_settings) == (
        f"Settings(repositories={repositories}, backup_path={str(backup_path.expanduser())!r})"
    )


def test_settings_to_dict(backup_path, repositories, settings_dict):
    test_settings = settings.Settings(repositories=repositories, backup_path=backup_path)

    assert test_settings.to_dict() == settings_dict


def test_load_settings_from_json(backup_path, repositories, settings_path):
    test_settings = settings.Settings.from_json(settings_path)

    assert str(test_settings.backup_path) == str(backup_path.expanduser())
    assert test_settings.repositories == repositories


def test_load_settings_from_json_with_error(caplog, settings_path):
    settings_path.unlink()

    with caplog.at_level(logging.ERROR):
        with pytest.raises(exceptions.FileSystemError) as error:
            settings.Settings.from_json(settings_path)

    message = "It is impossible to load the settings from the determined location."
    assert message in caplog.text
    assert str(error.value) == (
        f"Failed to load the settings from the provided path: {str(settings_path)!r}."
    )


def test_load_settings_from_json_with_decode_error(caplog, settings_path):
    settings_path.write_text("")

    with caplog.at_level(logging.ERROR):
        with pytest.raises(exceptions.SettingsError) as error:
            settings.Settings.from_json(settings_path)

    message = "The settings data you are trying to parse may be corrupt or incomplete."
    assert message in caplog.text
    assert str(error.value) == (
        f"Failed to parse the settings data from the provided path: {str(settings_path)!r}."
    )


def test_validation_during_load_settings(settings_path):
    settings_path.write_text(json.dumps({}))

    with pytest.raises(exceptions.SettingsError) as error:
        settings.Settings.from_json(settings_path)

    assert str(error.value) == "File does not match expected schema."
