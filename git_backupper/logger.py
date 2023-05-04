# Copyright 2023 (c) Vladislav Punko <iam.vlad.punko@gmail.com>

import logging
import logging.config

__all__ = ["setup"]


def setup(level: int = logging.WARNING) -> None:
    logging.config.dictConfig(
        {
            "formatters": {
                "default": {
                    "format": "%(levelname)s :: %(name)s :: %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "default",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "": {
                    "handlers": ["console"],
                    "level": level,
                },
            },
            "version": 1,
        }
    )
