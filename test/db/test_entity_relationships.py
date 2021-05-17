import warnings

import pytest


class TestEntityRelationships:
    @pytest.mark.parametrize(
        "endpoint_type, input_include_field, relationship",
        [
            pytest.param("applications", "jobs", "0,*", id="Jobs on /applications"),
            pytest.param(
                "applications", "facility", "1,1", id="Facility on /applications",
            ),
            pytest.param(
                "datacollections",
                "parameters",
                "0,*",
                id="DataCollectionParameters on /datacollections",
            ),
            pytest.param(
                "datacollections",
                "dataCollectionDatafiles",
                "0,*",
                id="DataCollectionDatafiles on /datacollections",
            ),
            pytest.param(
                "datacollections", "jobs", "0,*", id="Jobs on /datacollections",
            ),
            pytest.param(
                "datacollections",
                "dataCollectionDatasets",
                "0,*",
                id="DataCollectionDatasets on /datacollections",
            ),
            pytest.param(
                "datacollectiondatafiles",
                "dataCollection",
                "1,1",
                id="DataCollection on /datacollectiondatafiles",
            ),
            pytest.param(
                "datacollectiondatafiles",
                "datafile",
                "1,1",
                id="Datafile on /datacollectiondatafiles",
            ),
            pytest.param(
                "investigations", "samples", "0,*", id="Samples on /investigations",
            ),
        ],
    )
    def test_valid_related_entites(
        self,
        flask_test_app_db,
        valid_db_credentials_header,
        endpoint_type,
        input_include_field,
        relationship,
    ):
        test_response = flask_test_app_db.get(
            f'/{endpoint_type}?include="{input_include_field}"&limit=1',
            headers=valid_db_credentials_header,
        )
        print(test_response)

        if test_response.json == []:
            warnings.warn(f"No data returned from: {endpoint_type}")
        else:
            print(test_response.json[0])
            assert input_include_field in test_response.json[0].keys()

            if relationship == "0,*":
                assert isinstance(test_response.json[0][input_include_field], list)
            elif relationship == "1,1" or relationship == "0,1":
                assert isinstance(test_response.json[0][input_include_field], dict)
