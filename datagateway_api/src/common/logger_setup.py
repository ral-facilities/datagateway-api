"""
Module for setting up and configuring the logging system.
"""

import logging
import logging.config
from pathlib import Path

LOGGING_CONFIG_FILE_PATH = Path(__file__).parent.parent / "logging.ini"


def setup_logger() -> None:
    """
    Set up the logger using the configuration INI file.
    """
    logging.config.fileConfig(LOGGING_CONFIG_FILE_PATH)
