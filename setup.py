#!/usr/bin/env python

# -*- coding: utf-8 -*-

# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import pathlib

import setuptools

long_description = pathlib.Path("README.md").read_text()

setuptools.setup(
    name="git-mirrors",
    version=None,
    use_scm_version=True,
    description="Simplest way to mirror and restore git repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Vladislav Punko",
    author_email="iam.vlad.punko@gmail.com",
    license="MIT",
    url="https://github.com/vladpunko/git-mirrors",
    project_urls={
        "Issue tracker": "https://github.com/vladpunko/git-mirrors/issues",
        "Source code": "https://github.com/vladpunko/git-mirrors",
    },
    python_requires=">=3.8",
    install_requires=["setuptools>=60", "setuptools-scm>=8.0"],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=5.0.0",
            "isort>=5.0.0",
            "pre-commit>=3.0.0",
        ],
        "test": [
            "coverage>=7.0.0",
            "tox>=4.0.0",
        ],
    },
    packages=["git_mirrors", "git_mirrors/settings"],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development",
        "Topic :: Utilities",
        "Typing :: Typed",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    scripts=["git_mirrors/git-make-mirror"],
    entry_points={
        "console_scripts": [
            "git-make-mirrors = git_mirrors.__main__:main",
        ]
    },
)
