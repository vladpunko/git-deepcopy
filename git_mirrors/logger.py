# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import logging
import logging.config

from git_mirrors import defaults

__all__ = ["setup"]


def setup(level: int = logging.INFO) -> None:
    logging.config.dictConfig(
        {
            "disable_existing_loggers": False,
            "formatters": {
                "default": {
                    "datefmt": "%Y-%m-%d--%H-%M-%S",
                    "format": "%(asctime)s - %(levelname)s :: %(name)s :: %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stderr",
                },
                "logfile": {
                    "backupCount": 2,
                    "class": "logging.handlers.RotatingFileHandler",
                    "encoding": "utf-8",
                    "filename": defaults.LOGGING_PATH,
                    "formatter": "default",
                    "maxBytes": 50 * 1024 * 1024,  # ~50 MB
                    "mode": "at",
                },
            },
            "loggers": {
                "git_mirrors": {
                    "handlers": ["console", "logfile"],
                    "level": level,
                },
            },
            "version": 1,
        }
    )
