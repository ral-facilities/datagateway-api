import logging

from icat.client import Client
from object_pool import ObjectPool

from datagateway_api.common.config import Config

log = logging.getLogger()


class ICATClient(Client):
    """Wrapper class to allow an object pool of client objects to be created"""

    def __init__(self):
        super().__init__(Config.config.icat.url, checkCert=Config.config.icat.check_cert)
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
        min_init=Config.config.icat.client_pool_init_size,
        max_capacity=Config.config.icat.client_pool_max_size,
        max_reusable=0,
        expires=0,
    )
