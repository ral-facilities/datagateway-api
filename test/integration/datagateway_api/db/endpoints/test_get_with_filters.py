import pytest

from datagateway_api.src.common.config import Config
from datagateway_api.src.common.constants import Constants
from datagateway_api.src.common.date_handler import DateHandler


class TestDBGetWithFilters:
    def test_valid_get_with_filters(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        single_investigation_test_data_db,
    ):
        test_response = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/investigations?where="
            '{"title": {"like": "Title for DataGateway API Testing (DB)"}}',
            headers=valid_db_credentials_header,
        )

        assert test_response.json == [single_investigation_test_data_db.to_dict()]

    def test_valid_no_results_get_with_filters(
        self, flask_test_app_db, valid_db_credentials_header,
    ):
        test_response = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/investigations?where="
            '{"title": {"eq": "This filter should cause a 404 fortesting '
            'purposes..."}}',
            headers=valid_db_credentials_header,
        )

        assert test_response.json == []

    @pytest.mark.usefixtures("multiple_investigation_test_data_db")
    def test_valid_get_with_filters_multiple_distinct(
        self, flask_test_app_db, valid_db_credentials_header,
    ):
        test_response = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/investigations?where="
            '{"title": {"like": "Title for DataGateway API Testing (DB)"}}'
            '&distinct="title"',
            headers=valid_db_credentials_header,
        )

        expected = [
            {"title": f"Title for DataGateway API Testing (DB) {i}"} for i in range(5)
        ]

        assert test_response.json == expected

    @pytest.mark.parametrize(
        "distinct_param, expected_response",
        [
            pytest.param(
                '"title"',
                [{"title": "Title for DataGateway API Testing (DB) 0"}],
                id="Single unrelated distinct field",
            ),
            pytest.param(
                '"investigationInstruments.createTime"',
                [
                    {
                        "investigationInstruments": {
                            "createTime": DateHandler.datetime_object_to_str(
                                Constants.TEST_MOD_CREATE_DATETIME,
                            ),
                        },
                    },
                ],
                id="Single related distinct field",
            ),
            pytest.param(
                '["createTime", "investigationInstruments.createTime"]',
                [
                    {
                        "createTime": DateHandler.datetime_object_to_str(
                            Constants.TEST_MOD_CREATE_DATETIME,
                        ),
                        "investigationInstruments": {
                            "createTime": DateHandler.datetime_object_to_str(
                                Constants.TEST_MOD_CREATE_DATETIME,
                            ),
                        },
                    },
                ],
                id="Single related distinct field with unrelated field",
            ),
            pytest.param(
                '["investigationInstruments.createTime", "facility.id"]',
                [
                    {
                        "facility": {"id": 1},
                        "investigationInstruments": {
                            "createTime": DateHandler.datetime_object_to_str(
                                Constants.TEST_MOD_CREATE_DATETIME,
                            ),
                        },
                    },
                ],
                id="Multiple related distinct fields",
            ),
            pytest.param(
                '["createTime", "investigationInstruments.createTime", "facility.id"]',
                [
                    {
                        "createTime": DateHandler.datetime_object_to_str(
                            Constants.TEST_MOD_CREATE_DATETIME,
                        ),
                        "facility": {"id": 1},
                        "investigationInstruments": {
                            "createTime": DateHandler.datetime_object_to_str(
                                Constants.TEST_MOD_CREATE_DATETIME,
                            ),
                        },
                    },
                ],
                id="Multiple related distinct fields with unrelated field",
            ),
        ],
    )
    @pytest.mark.usefixtures("related_distinct_data_db")
    def test_valid_get_with_filters_related_distinct(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        distinct_param,
        expected_response,
    ):
        test_response = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/investigations?where="
            '{"title": {"like": "Title for DataGateway API Testing (DB)"}}'
            f"&distinct={distinct_param}",
            headers=valid_db_credentials_header,
        )

        print(test_response.json)

        assert test_response.json == expected_response

    def test_limit_skip_merge_get_with_filters(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        multiple_investigation_test_data_db,
    ):
        skip_value = 1
        limit_value = 2

        test_response = flask_test_app_db.get(
            f"{Config.config.datagateway_api.extension}/investigations?where="
            '{"title": {"like": "Title for DataGateway API Testing (DB)"}}'
            f'&skip={skip_value}&limit={limit_value}&order="id ASC"',
            headers=valid_db_credentials_header,
        )

        # Copy required to ensure data is deleted at the end of the test
        investigation_test_data_copy = multiple_investigation_test_data_db.copy()
        filtered_investigation_data = []
        filter_count = 0
        while filter_count < limit_value:
            filtered_investigation_data.append(
                investigation_test_data_copy.pop(skip_value).to_dict(),
            )
            filter_count += 1

        assert test_response.json == filtered_investigation_data
