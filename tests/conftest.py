# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import hashlib
import pathlib
import uuid

import pytest


@pytest.fixture
def directory_path(fs):
    path = pathlib.Path("directory")
    fs.create_dir(path)

    return path


@pytest.fixture
def symlink_path(directory_path, fs):
    path = directory_path / "symlink.link"
    fs.create_symlink(path, directory_path)

    return path


@pytest.fixture
def file_path(directory_path, fs):
    path = directory_path / "test.tmp"
    fs.create_file(path)

    return path


@pytest.fixture
def checksums(directory_path):
    data = {}

    for _ in range(5):
        path = directory_path / str(uuid.uuid4())
        path.write_text(path.name)

        data[path] = hashlib.sha256(path.read_bytes()).hexdigest()

    return data
