import pytest

from datagateway_api.src.datagateway_api.backend import Backend
from datagateway_api.src.datagateway_api.backends import create_backend
from datagateway_api.src.datagateway_api.database.backend import DatabaseBackend
from datagateway_api.src.datagateway_api.icat.backend import PythonICATBackend


class TestBackends:
    @pytest.mark.parametrize(
        "backend_name, backend_type",
        [
            pytest.param("db", DatabaseBackend, id="Database Backend"),
            pytest.param("python_icat", PythonICATBackend, id="Python ICAT Backend"),
        ],
    )
    def test_valid_backend_creation(self, backend_name, backend_type):
        test_backend = create_backend(backend_name)

        assert type(test_backend) == backend_type

    def test_invalid_backend_creation(self):
        with pytest.raises(SystemExit):
            create_backend("invalid_backend_name")

    def test_abstract_class(self):
        """
        Test the `Backend` abstract class has all required abstract methods for the API
        """
        Backend.__abstractmethods__ = set()

        class DummyBackend(Backend):
            pass

        d = DummyBackend()

        credentials = "credentials"
        session_id = "session_id"
        entity_type = "entity_type"
        filters = "filters"
        data = "data"
        id_ = "id_"

        assert d.ping() is None
        assert d.login(credentials) is None
        assert d.get_session_details(session_id) is None
        assert d.refresh(session_id) is None
        assert d.logout(session_id) is None
        assert d.get_with_filters(session_id, entity_type, filters) is None
        assert d.create(session_id, entity_type, data) is None
        assert d.update(session_id, entity_type, data) is None
        assert d.get_one_with_filters(session_id, entity_type, filters) is None
        assert d.count_with_filters(session_id, entity_type, filters) is None
        assert d.get_with_id(session_id, entity_type, id_) is None
        assert d.delete_with_id(session_id, entity_type, id_) is None
        assert d.update_with_id(session_id, entity_type, id_, data) is None
