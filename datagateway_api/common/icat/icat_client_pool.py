import logging

from icat.client import Client
from object_pool import ObjectPool

from datagateway_api.common.config import config

log = logging.getLogger()


class ICATClient(Client):
    """Wrapper class to allow an object pool of client objects to be created"""

    def __init__(self):
        super().__init__(config.get_icat_url(), checkCert=config.get_icat_check_cert())
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
        ICATClient, min_init=5, max_capacity=20, max_reusable=0, expires=0,
    )


class ClientPoolExecutor(ObjectPool.Executor):
    """TODO"""

    def __init__(self, klass):
        # klass is the instance of object pool
        self.__pool = klass
        self.client, self.resource_stats = None

    def get_client(self):
        self.client, self.resource_stats = self.__pool._get_resource()
        return self.client

    def release_client(self):
        self.__pool._queue_resource(self.client, self.resource_stats)


def get_executor(client_pool):
    return ClientPoolExecutor(client_pool)
