import logging.config


log_level = "DEBUG"
LOG_FILE_NAME = "../logs.log"
logger_config = {
    "version": 1,
    "formatters": {"default": {
        "format": "[%(asctime)s] {%(module)s:%(filename)s:%(funcName)s:%(lineno)d} %(levelname)s -%(message)s  ",
    }},
    "handlers": {"default": {
        "level": "DEBUG",
        "formatter": "default",
        "class": "logging.handlers.RotatingFileHandler",
        "filename": LOG_FILE_NAME,
        "maxBytes": 5000000,
        "backupCount": 10
    }},
    "root": {
        "level": log_level,
        "handlers": ["default"]
    }
}


def setup_logger():
    logging.config.dictConfig(logger_config)