import json

import datagateway_api.src.search_api.models as models


class TestModels:
    def test_from_icat_person_model(self):
        expected_model_data = {
            "id": "1",
            "fullName": "Test fullname",
            "orcid": "1111",
            "researcherId": None,
            "firstName": "Test given name",
            "lastName": "Test family name",
            "members": None,
        }
        # TODO: `id` is returned as `int` from ICAT whereas Person model expects `str`
        icat_data = {
            "id": "1",
            "fullName": "Test fullname",
            "orcidId": "1111",
            "givenName": "Test given name",
            "familyName": "Test family name",
        }

        person_model = models.Person.from_icat(icat_data)

        assert person_model.json(by_alias=True) == json.dumps(expected_model_data)
