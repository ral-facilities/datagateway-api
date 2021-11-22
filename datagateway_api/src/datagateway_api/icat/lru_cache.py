import logging

from cachetools.lru import LRUCache

from datagateway_api.src.common.config import config

log = logging.getLogger()


class ExtendedLRUCache(LRUCache):
    """
    An extension to cachetools' LRUCache class to allow client objects to be pushed back
    into the pool

    This version of LRU cache was chosen instead of the builtin LRU cache as it allows
    for addtional actions to be added when an item leaves the cache (controlled by
    `popitem()`). Since the builtin version was just a function (using a couple of
    wrapper functions), adding additional functionality wasn't possible.
    """

    def __init__(self):
        super().__init__(maxsize=config.datagateway_api.client_cache_size)

    def popitem(self):
        key, client = super().popitem()
        session_id, client_pool = key
        log.debug("Client popped from LRU cache with session: %s", session_id)

        # Flushing session ID so next time the client object is used, there's no issues
        client.sessionId = None

        # Put client back into pool - resource stats aren't used in the API, so defaults
        # are passed in
        client_pool._queue_resource(client, client_pool._get_default_stats())
