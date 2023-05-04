# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import logging
import logging.config
import os
import tempfile

__all__ = ["setup"]


def setup(level: int = logging.WARNING) -> None:
    logging.config.dictConfig(
        {
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "format": "%(asctime)s - %(levelname)s :: %(name)s :: %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
                "logfile": {
                    "class": "logging.FileHandler",
                    "encoding": "utf-8",
                    "filename": os.path.join(tempfile.gettempdir(), "git-backupper.log"),
                    "formatter": "default",
                    "mode": "at",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["console", "logfile"],
                    "level": level,
                },
            },
            "version": 1,
        }
    )
