import logging.config
from pathlib import Path

from datagateway_api.src.common.config import Config

LOG_FILE_NAME = Path(Config.config.log_location)
logger_config = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] {%(module)s:%(filename)s:%(funcName)s:%(lineno)d}"
            " %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "level": Config.config.log_level,
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE_NAME,
            "maxBytes": 5000000,
            "backupCount": 10,
        },
    },
    "root": {"level": Config.config.log_level, "handlers": ["default"]},
}


def setup_logger():
    logging.config.dictConfig(logger_config)
