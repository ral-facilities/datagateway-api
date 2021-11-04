import logging

from icat.client import Client
from object_pool import ObjectPool

from datagateway_api.common.config import config

log = logging.getLogger()


class ICATClient(Client):
    """Wrapper class to allow an object pool of client objects to be created"""

    def __init__(self):
        super().__init__(
            config.datagateway_api.icat_url,
            checkCert=config.datagateway_api.icat_check_cert,
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
        min_init=config.datagateway_api.client_pool_init_size,
        max_capacity=config.datagateway_api.client_pool_max_size,
        max_reusable=0,
        expires=0,
    )
