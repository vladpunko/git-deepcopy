# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import json
import logging
import pathlib

import pytest

from git_mirrors import exceptions
from git_mirrors.settings import settings


@pytest.fixture
def repositories():
    return ["1.git", "2.git", "3.git"]


@pytest.fixture
def storage_path():
    path = pathlib.Path("~/directory")

    return path


@pytest.fixture
def settings_path(repositories, storage_path, fs):
    path = pathlib.Path("settings.json")
    path.write_text(json.dumps({"repositories": repositories, "storage_path": str(storage_path)}))

    return path


@pytest.fixture
def settings_dict(repositories, storage_path):
    return {"repositories": repositories, "storage_path": storage_path.expanduser()}


def test_settings_class(repositories, storage_path, settings_dict):
    test_settings = settings.Settings(repositories=repositories * 5, storage_path=storage_path)

    assert str(test_settings.storage_path) == str(storage_path.expanduser())
    assert test_settings.repositories == repositories

    assert str(test_settings) == json.dumps(settings_dict, default=str, indent=2)
    assert repr(test_settings) == (
        f"Settings(repositories={repositories}, storage_path={str(storage_path.expanduser())!r})"
    )


def test_settings_to_dict(repositories, storage_path, settings_dict):
    test_settings = settings.Settings(repositories=repositories, storage_path=storage_path)

    assert test_settings.to_dict() == settings_dict


def test_load_settings_from_json(repositories, storage_path, settings_path):
    test_settings = settings.Settings.from_json(settings_path)

    assert str(test_settings.storage_path) == str(storage_path.expanduser())
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
