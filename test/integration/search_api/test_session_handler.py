from datagateway_api.src.datagateway_api.icat.icat_client_pool import ICATClient
from datagateway_api.src.search_api.session_handler import (
    client_manager,
    SessionHandler,
)


class TestSessionHandler:
    def test_session_handler_class(self):
        assert isinstance(SessionHandler.client, ICATClient)

    def test_client_manager_decorator(self):
        @client_manager
        def manage_client():
            pass

        # Checks that the decorator assigns a session ID, checking one is not present
        # before the decorator runs
        assert not SessionHandler.client.sessionId
        manage_client()
        assert SessionHandler.client.sessionId
