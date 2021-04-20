import logging.config
from pathlib import Path

from datagateway_api.common.config import APIConfigOptions, config

LOG_FILE_NAME = Path(config.get_config_value(APIConfigOptions.LOG_LOCATION))
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
            "level": config.get_config_value(APIConfigOptions.LOG_LEVEL),
            "formatter": "default",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_FILE_NAME,
            "maxBytes": 5000000,
            "backupCount": 10,
        },
    },
    "root": {
        "level": config.get_config_value(APIConfigOptions.LOG_LEVEL),
        "handlers": ["default"],
    },
}


def setup_logger():
    logging.config.dictConfig(logger_config)
