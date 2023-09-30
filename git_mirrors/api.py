# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import logging
import pathlib
import typing

from git_mirrors import cache, defaults, fs, repository

logger = logging.getLogger("git_mirrors")

__all__ = ["mirror"]


def mirror(
    repositories: typing.List[str],
    storage_path: pathlib.Path,
    cache_path: pathlib.Path = defaults.CACHE_PATH,
) -> None:
    if not storage_path.is_dir():
        fs.create_directory(storage_path)

    for repository_url in repositories:
        repository_mirror = repository.Repository.from_url(
            parent_path=storage_path, url=repository_url
        )
        logger.info("Processing the '%s' repository.", repository_mirror.url)

        if not repository_mirror.exists_on_remote():
            logger.warning(
                "The remote repository could not be detected for: '%s'.",
                repository_mirror.url,
            )
            continue

        with cache.PersistentCache(path=cache_path) as application_cache:
            # Step -- 1.
            if repository_mirror in application_cache and repository_mirror.exists_locally():
                checksums = fs.calculate_checksums(repository_mirror.local_path)

                if application_cache[repository_mirror] == checksums:
                    repository_mirror.update_local_copy()  # git fetch
                    application_cache[repository_mirror].update(checksums)
                else:
                    logger.warning(
                        "The '%s' repository is corrupted.",
                        str(repository_mirror.local_path),
                    )
                    if repository_mirror.local_path.is_dir():
                        fs.remove_directory(repository_mirror.local_path)

            # Step -- 2.
            if repository_mirror not in application_cache and (
                repository_mirror.local_path.is_dir() and not repository_mirror.exists_locally()
            ):
                fs.remove_directory(repository_mirror.local_path)

            # Step -- 3.
            if not repository_mirror.local_path.is_dir():
                repository_mirror.create_local_copy()  # git clone
                repository_mirror.update_local_copy()  # git fetch -> FETCH_HEAD
                application_cache[repository_mirror] = fs.calculate_checksums(
                    repository_mirror.local_path
                )

        logger.info("Mirror for the '%s' repository has been created.", repository_mirror.url)
