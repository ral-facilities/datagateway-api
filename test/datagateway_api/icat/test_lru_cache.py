from unittest.mock import MagicMock

from cachetools import cached
from icat.client import Client

from datagateway_api.common.config import APIConfigOptions, config
from datagateway_api.common.datagateway_api.icat.icat_client_pool import (
    create_client_pool,
)
from datagateway_api.common.datagateway_api.icat.lru_cache import ExtendedLRUCache


class TestLRUCache:
    def test_valid_cache_creation(self):
        test_cache = ExtendedLRUCache()
        assert test_cache.maxsize == config.get_config_value(
            APIConfigOptions.CLIENT_CACHE_SIZE,
        )

    def test_valid_popitem(self):
        test_cache = ExtendedLRUCache()
        test_pool = create_client_pool()
        test_client = Client(
            config.get_config_value(APIConfigOptions.ICAT_URL),
            checkCert=config.get_config_value(APIConfigOptions.ICAT_CHECK_CERT),
        )

        test_cache.popitem = MagicMock(side_effect=test_cache.popitem)

        @cached(cache=test_cache)
        def get_cached_client(cache_number, client_pool):
            return test_client

        for cache_number in range(
            config.get_config_value(APIConfigOptions.CLIENT_CACHE_SIZE) + 1,
        ):
            get_cached_client(cache_number, test_pool)

        assert test_cache.popitem.called
