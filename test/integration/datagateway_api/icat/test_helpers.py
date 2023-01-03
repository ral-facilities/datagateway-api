from unittest.mock import patch

from icat.exception import ICATInternalError
import pytest

from datagateway_api.src.common.exceptions import PythonICATError
from datagateway_api.src.datagateway_api.icat.helpers import push_data_updates_to_icat


class TestICATHelpers:
    """Testing the helper functions which aren't covered in the endpoint tests"""

    def test_invalid_update_pushes(self, icat_client):
        with patch(
            "icat.entity.Entity.update",
            side_effect=ICATInternalError("Mocked Exception"),
        ):
            inv_entity = icat_client.new("investigation", name="Investigation A")
            with pytest.raises(PythonICATError):
                push_data_updates_to_icat(inv_entity)
