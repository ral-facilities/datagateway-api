import pytest

from datagateway_api.common.backends import create_backend
from datagateway_api.common.database.backend import DatabaseBackend
from datagateway_api.common.icat.backend import PythonICATBackend


class TestBackends:
    @pytest.mark.parametrize(
        "backend_name, backend_type",
        [
            pytest.param("db", DatabaseBackend, id="Database Backend"),
            pytest.param("python_icat", PythonICATBackend, id="Python ICAT Backend"),
        ],
    )
    def test_backend_creation(self, backend_name, backend_type):
        test_backend = create_backend(backend_name)

        assert type(test_backend) == backend_type
