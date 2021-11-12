import logging

from icat.client import Client
from object_pool import ObjectPool

from datagateway_api.src.common.config import APIConfigOptions, config

log = logging.getLogger()


class ICATClient(Client):
    """Wrapper class to allow an object pool of client objects to be created"""

    def __init__(self):
        super().__init__(
            config.get_config_value(APIConfigOptions.ICAT_URL),
            checkCert=config.get_config_value(APIConfigOptions.ICAT_CHECK_CERT),
        )
        # When clients are cleaned up, sessions won't be logged out
        self.autoLogout = False

    def clean_up(self):
        """
        Allows object pool to cleanup the client's resources, using the existing Python
        ICAT functionality
        """
        super().cleanup()


def create_client_pool():
    """
    Function to create an object pool for ICAT client objects

    The ObjectPool class uses the singleton design pattern
    """

    return ObjectPool(
        ICATClient,
        min_init=config.get_config_value(APIConfigOptions.CLIENT_POOL_INIT_SIZE),
        max_capacity=config.get_config_value(APIConfigOptions.CLIENT_POOL_MAX_SIZE),
        max_reusable=0,
        expires=0,
    )
