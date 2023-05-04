# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import logging
import pathlib

from git_backupper import cache, defaults, fs, repository

logger = logging.getLogger(__name__)

__all__ = ["backup"]


def backup(
    backup_path: pathlib.Path,
    repositories: list[str],
    cache_path: pathlib.Path = defaults.CACHE_PATH,
) -> None:
    if not backup_path.is_dir():
        fs.create_directory(backup_path)

    for repository_url in repositories:
        backup_repository = repository.Repository.from_url(
            parent_path=backup_path, url=repository_url
        )

        if not backup_repository.exists_on_remote():
            logger.warning(
                "The remote repository could not be detected for: '%s'.", backup_repository.url
            )
            continue

        with cache.PersistentCache(path=cache_path) as backup_cache:
            # Step -- 1.
            if backup_repository in backup_cache and backup_repository.exists_locally():
                checksums = fs.calculate_checksums(backup_repository.local_path)

                if backup_cache[backup_repository] == checksums:
                    backup_repository.update_local_copy()  # git fetch
                    backup_cache[backup_repository].update(checksums)
                else:
                    logger.warning(
                        "The '%s' repository is corrupted.", str(backup_repository.local_path)
                    )
                    if backup_repository.local_path.is_dir():
                        fs.remove_directory(backup_repository.local_path)

            # Step -- 2.
            if backup_repository not in backup_cache and (
                backup_repository.local_path.is_dir() and not backup_repository.exists_locally()
            ):
                fs.remove_directory(backup_repository.local_path)

            # Step -- 3.
            if not backup_repository.local_path.is_dir():
                backup_repository.create_local_copy()  # git clone
                backup_repository.update_local_copy()  # git fetch -> FETCH_HEAD
                backup_cache[backup_repository] = fs.calculate_checksums(
                    backup_repository.local_path
                )
