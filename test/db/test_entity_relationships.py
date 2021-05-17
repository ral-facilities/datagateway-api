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
                "datacollectiondatasets",
                "dataset",
                "1,1",
                id="Dataset on /datacollectiondatasets",
            ),
            pytest.param(
                "datacollectiondatasets",
                "dataCollection",
                "1,1",
                id="DataCollection on /datacollectiondatasets",
            ),
            pytest.param(
                "datacollectionparameters",
                "type",
                "1,1",
                id="ParameterType on /datacollectionparameters",
            ),
            pytest.param(
                "datacollectionparameters",
                "dataCollection",
                "1,1",
                id="DataCollection on /datacollectionparameters",
            ),
            pytest.param(
                "datafiles", "datafileFormat", "0,1", id="DatafileFormat on /datafiles",
            ),
            pytest.param(
                "datafiles",
                "dataCollectionDatafiles",
                "0,*",
                id="DataCollectionDatafiles on /datafiles",
            ),
            # TODO - RelatedDatafiles on /datafiles
            pytest.param("datafiles", "dataset", "1,1", id="Dataset on /datafiles"),
            pytest.param(
                "datafiles", "parameters", "0,*", id="DatafileParameters on /datafiles",
            ),
            pytest.param(
                "datafileformats",
                "datafiles",
                "0,*",
                id="Datafiles on /datafileformats",
            ),
            pytest.param(
                "datafileformats", "facility", "1,1", id="Facility on /datafileformats",
            ),
            pytest.param(
                "datafileparameters",
                "type",
                "1,1",
                id="ParameterTypes on /datafileparameters",
            ),
            pytest.param(
                "datafileparameters",
                "datafile",
                "1,1",
                id="Datafiles on /datafileparameters",
            ),
            pytest.param(
                "datasets", "parameters", "0,*", id="DatasetParameters on /datasets",
            ),
            pytest.param("datasets", "datafiles", "0,*", id="Datafiles on /datasets"),
            pytest.param(
                "datasets",
                "dataCollectionDatasets",
                "0,*",
                id="DataCollectionDatasets on /datasets",
            ),
            pytest.param("datasets", "sample", "0,1", id="Sample on /datasets"),
            pytest.param(
                "datasets", "investigation", "1,1", id="Investigation on /datasets",
            ),
            pytest.param("datasets", "type", "1,1", id="DatasetType on /datasets"),
            pytest.param(
                "datasetparameters",
                "type",
                "1,1",
                id="ParameterType on /datasetparameters",
            ),
            pytest.param(
                "datasetparameters",
                "dataset",
                "1,1",
                id="Dataset on /datasetparameters",
            ),
            pytest.param(
                "datasettypes", "facility", "1,1", id="Facility on /datasettypes",
            ),
            pytest.param(
                "datasettypes", "datasets", "0,*", id="Datasets on /datasettypes",
            ),
            pytest.param(
                "facilities",
                "facilityCycles",
                "0,*",
                id="FacilityCycles on /facilities",
            ),
            pytest.param(
                "facilities", "applications", "0,*", id="Applications on /facilities",
            ),
            pytest.param(
                "facilities",
                "investigations",
                "0,*",
                id="Investigations on /facilities",
            ),
            pytest.param(
                "facilities", "datasetTypes", "0,*", id="DatasetTypes on /facilities",
            ),
            pytest.param(
                "facilities",
                "investigationTypes",
                "0,*",
                id="InvestigationTypes on /facilities",
            ),
            pytest.param(
                "facilities", "instruments", "0,*", id="Instruments on /facilities",
            ),
            pytest.param(
                "facilities", "sampleTypes", "0,*", id="SampleTypes on /facilities",
            ),
            pytest.param(
                "facilities",
                "parameterTypes",
                "0,*",
                id="ParameterTypes on /facilities",
            ),
            pytest.param(
                "facilities",
                "datafileFormats",
                "0,*",
                id="DatafileFormats on /facilities",
            ),
            pytest.param(
                "facilitycycles", "facility", "1,1", id="Facility on /facilitycycles",
            ),
            pytest.param(
                "groupings", "userGroups", "0,*", id="UserGroups on /groupings",
            ),
            pytest.param(
                "groupings",
                "investigationGroups",
                "0,*",
                id="InvestigationGroups on /groupings",
            ),
            pytest.param("groupings", "rules", "0,*", id="Rules on /groupings"),
            pytest.param(
                "instruments", "facility", "1,1", id="Facility on /instruments",
            ),
            pytest.param(
                "instruments",
                "instrumentScientists",
                "0,*",
                id="InstrumentScientists on /instruments",
            ),
            pytest.param(
                "instruments",
                "investigationInstruments",
                "0,*",
                id="InvestigationInstruments on /instruments",
            ),
            pytest.param(
                "instrumentscientists",
                "user",
                "1,1",
                id="User on /instrumentscientists",
            ),
            pytest.param(
                "instrumentscientists",
                "instrument",
                "1,1",
                id="Instrument on /instrumentscientists",
            ),
            pytest.param(
                "investigations",
                "parameters",
                "0,*",
                id="InvestigationParameters on /investigations",
            ),
            pytest.param(
                "investigations",
                "studyInvestigations",
                "0,*",
                id="StudyInvestigations on /investigations",
            ),
            pytest.param(
                "investigations", "datasets", "0,*", id="Datasets on /investigations",
            ),
            pytest.param(
                "investigations", "keywords", "0,*", id="Keywords on /investigations",
            ),
            pytest.param(
                "investigations", "samples", "0,*", id="Samples on /investigations",
            ),
            pytest.param(
                "investigations", "shifts", "0,*", id="Shifts on /investigations",
            ),
            pytest.param(
                "investigations",
                "investigationInstruments",
                "0,*",
                id="InvestigationInstruments on /investigations",
            ),
            pytest.param(
                "investigations", "facility", "1,1", id="Facility on /investigations",
            ),
            pytest.param(
                "investigations",
                "investigationGroups",
                "0,*",
                id="InvestigationGroups on /investigations",
            ),
            pytest.param(
                "investigations",
                "investigationUsers",
                "0,*",
                id="InvestigationUsers on /investigations",
            ),
            pytest.param(
                "investigations",
                "publications",
                "0,*",
                id="Publications on /investigations",
            ),
            pytest.param(
                "investigations",
                "type",
                "1,1",
                id="InvestigationType on /investigations",
            ),
            pytest.param(
                "investigationgroups",
                "investigation",
                "1,1",
                id="Investigation on /investigationgroups",
            ),
            pytest.param(
                "investigationgroups",
                "grouping",
                "1,1",
                id="Grouping on /investigationgroups",
            ),
            pytest.param(
                "investigationinstruments",
                "investigation",
                "1,1",
                id="Investigation on /investigationinstruments",
            ),
            pytest.param(
                "investigationinstruments",
                "instrument",
                "1,1",
                id="Instrument on /investigationinstruments",
            ),
            pytest.param(
                "investigationparameters",
                "investigation",
                "1,1",
                id="Investigation on /investigationparameters",
            ),
            pytest.param(
                "investigationparameters",
                "type",
                "1,1",
                id="ParameterType on /investigationparameters",
            ),
            pytest.param(
                "investigationtypes",
                "investigations",
                "0,*",
                id="Investigations on /investigationtypes",
            ),
            pytest.param(
                "investigationtypes",
                "facility",
                "1,1",
                id="Facility on /investigationtypes",
            ),
            pytest.param(
                "investigationusers",
                "investigation",
                "1,1",
                id="Investigation on /investigationusers",
            ),
            pytest.param(
                "investigationusers", "user", "1,1", id="User on /investigationusers",
            ),
            pytest.param("jobs", "application", "1,1", id="Application on /jobs"),
            # TODO - DataCollection on /jobs
            pytest.param(
                "keywords", "investigation", "1,1", id="Investigation on /keywords",
            ),
            pytest.param(
                "parametertypes",
                "investigationParameters",
                "0,*",
                id="InvestigationParameters on /parametertypes",
            ),
            pytest.param(
                "parametertypes", "facility", "1,1", id="Facility on /parametertypes",
            ),
            pytest.param(
                "parametertypes",
                "datasetParameters",
                "0,*",
                id="DatasetParameters on /parametertypes",
            ),
            pytest.param(
                "parametertypes",
                "sampleParameters",
                "0,*",
                id="SampleParameters on /parametertypes",
            ),
            pytest.param(
                "parametertypes",
                "permissibleStringValues",
                "0,*",
                id="PermissibleStringValues on /parametertypes",
            ),
            pytest.param(
                "parametertypes",
                "dataCollectionParameters",
                "0,*",
                id="DataCollectionParameters on /parametertypes",
            ),
            pytest.param(
                "parametertypes",
                "datafileParameters",
                "0,*",
                id="DatafileParameters on /parametertypes",
            ),
            pytest.param(
                "permissiblestringvalues",
                "type",
                "0,*",
                id="ParameterType on /permissiblestringvalues",
            ),
            pytest.param(
                "publications",
                "investigation",
                "1,1",
                id="Investigation on /publications",
            ),
            # TODO - Datafile on /relateddatafiles
            pytest.param("rules", "grouping", "0,1", id="Grouping on /rules"),
            pytest.param("samples", "type", "0,1", id="SampleType on /samples"),
            pytest.param(
                "samples", "investigation", "1,1", id="Investigtion on /samples",
            ),
            pytest.param("samples", "parameters", "0,*", id="Parameters on /samples"),
            pytest.param("samples", "datasets", "0,*", id="Datasets on /samples"),
            pytest.param(
                "sampletypes", "facility", "1,1", id="Facility on /sampletypes",
            ),
            pytest.param(
                "sampletypes", "samples", "0,*", id="Samples on /sampletypes",
            ),
            pytest.param(
                "shifts", "investigation", "1,1", id="Investigation on /shifts",
            ),
            pytest.param("studies", "user", "0,1", id="User on /studies"),
            pytest.param(
                "studies",
                "studyInvestigations",
                "0,*",
                id="StudyInvestigations on /studies",
            ),
            pytest.param(
                "studyinvestigations",
                "study",
                "1,1",
                id="Study on /studyinvestigations",
            ),
            pytest.param(
                "studyinvestigations",
                "investigation",
                "1,1",
                id="Investigation on /studyinvestigations",
            ),
            pytest.param(
                "users", "investigationUsers", "0,*", id="InvestigationUsers on /users",
            ),
            pytest.param("users", "userGroups", "0,*", id="UserGroups on /users"),
            pytest.param(
                "users",
                "instrumentScientists",
                "0,*",
                id="InstrumentScientists on /users",
            ),
            pytest.param("users", "studies", "0,*", id="Studies on /users"),
            pytest.param("usergroups", "user", "1,1", id="User on /usergroups"),
            pytest.param(
                "usergroups", "grouping", "1,1", id="Grouping on /usergroups",
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
