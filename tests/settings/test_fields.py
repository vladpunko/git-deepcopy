# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import pathlib

import pytest

from git_backupper import exceptions
from git_backupper.settings import fields


@pytest.fixture
def settings():
    class Settings:
        # schema
        path = fields.PathField()
        sequence = fields.SequenceField()

    return Settings()


def test_path_field(settings):
    path = pathlib.Path("~/directory")
    settings.path = path

    assert str(settings.path) == str(path.expanduser())


@pytest.mark.parametrize("path", ("", None, True, [], {}))
def test_validation_error_path_field(path, settings):
    with pytest.raises(exceptions.SettingsError):
        settings.path = path


def test_list_field(settings):
    sequence = ["1", "1", "2", "2", "3", "3"]
    settings.sequence = sequence

    assert settings.sequence == sorted(set(sequence))


@pytest.mark.parametrize("sequence", (b"", "", [1, 2, 3], [1, "2", "3"]))
def test_validation_error_sequence_field(sequence, settings):
    with pytest.raises(exceptions.SettingsError):
        settings.sequence = sequence


def test_fields_without_instance():
    class Test:
        path = fields.PathField()

    assert isinstance(Test.path, fields.PathField)
