#!/usr/bin/env python3

# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import argparse
import errno
import logging
import sys
from importlib.metadata import version

from git_backupper import api, defaults, exceptions, logger_wrapper, settings

logger_wrapper.setup()  # Set up the logging system.
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simplest way to back up and restore git repositories."
    )
    parser.add_argument("-v", "--version", action="version", version=version("git-backupper"))
    parser.add_argument(
        "-d",
        "--debug",
        action="store_const",
        const=logging.DEBUG,  # level must be an int or a str
        default=logging.WARNING,
        dest="logging_level",
        help="generate extensive debugging output during command execution",
    )

    try:
        arguments = parser.parse_args()

        # Assign a new severity level to the logging system.
        logger.setLevel(arguments.logging_level)

        # Step -- 1.
        application_settings = settings.Settings.from_json(path=defaults.SETTINGS_PATH)
        logger.warning(application_settings)

        # Step -- 2.
        api.backup(application_settings.backup_path, application_settings.repositories)
    except (
        exceptions.ExternalProcessError,
        exceptions.FileSystemError,
        exceptions.SettingsError,
    ) as err:
        logger.debug("An unexpected error occurred at this program runtime:", exc_info=True)
        # Stop this program runtime and return the exit status code.
        sys.exit(getattr(err, "errno", errno.EPERM))

    except KeyboardInterrupt as err:
        logger.error("Abort this program runtime as a consequence of a keyboard interrupt.")
        # Terminate the execution of this program due to a keyboard interruption.
        sys.exit(getattr(err, "errno", errno.EINTR))


if __name__ == "__main__":
    main()
