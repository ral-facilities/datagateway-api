from common.database.models import (
    APPLICATION,
    DATACOLLECTIONDATAFILE,
    DATACOLLECTIONPARAMETER,
    DATACOLLECTIONDATASET,
    DATACOLLECTION,
    DATAFILEFORMAT,
    DATAFILE,
    FACILITYCYCLE,
    DATASETTYPE,
    GROUPING,
    INSTRUMENT,
    INSTRUMENTSCIENTIST,
    INVESTIGATIONGROUP,
    INVESTIGATIONINSTRUMENT,
    INVESTIGATIONTYPE,
    INVESTIGATION,
    JOB,
    KEYWORD,
    PARAMETERTYPE,
    INVESTIGATIONPARAMETER,
    INVESTIGATIONUSER,
    PUBLICSTEP,
    RULE,
    SAMPLE,
    USERGROUP,
    STUDYINVESTIGATION,
    SAMPLETYPE,
    RELATEDDATAFILE,
    SAMPLEPARAMETER,
    PUBLICATION,
    STUDY,
    USER,
    SHIFT,
    PERMISSIBLESTRINGVALUE,
    FACILITY,
    DATAFILEPARAMETER,
    DATASET,
    DATASETPARAMETER,
)

import datetime
from sqlalchemy.inspection import inspect

endpoints = {
    "Applications": APPLICATION,
    "DataCollectionDatafiles": DATACOLLECTIONDATAFILE,
    "DataCollectionDatasets": DATACOLLECTIONDATASET,
    "DataCollectionParameters": DATACOLLECTIONPARAMETER,
    "DataCollections": DATACOLLECTION,
    "DatafileFormats": DATAFILEFORMAT,
    "DatafileParameters": DATAFILEPARAMETER,
    "Datafiles": DATAFILE,
    "DatasetParameters": DATASETPARAMETER,
    "DatasetTypes": DATASETTYPE,
    "Datasets": DATASET,
    "Facilities": FACILITY,
    "FacilityCycles": FACILITYCYCLE,
    "Groupings": GROUPING,
    "InstrumentScientists": INSTRUMENTSCIENTIST,
    "Instruments": INSTRUMENT,
    "InvestigationGroups": INVESTIGATIONGROUP,
    "InvestigationInstruments": INVESTIGATIONINSTRUMENT,
    "InvestigationParameters": INVESTIGATIONPARAMETER,
    "InvestigationTypes": INVESTIGATIONTYPE,
    "InvestigationUsers": INVESTIGATIONUSER,
    "Investigations": INVESTIGATION,
    "Jobs": JOB,
    "Keywords": KEYWORD,
    "ParameterTypes": PARAMETERTYPE,
    "PermissibleStringValues": PERMISSIBLESTRINGVALUE,
    "PublicSteps": PUBLICSTEP,
    "Publications": PUBLICATION,
    "RelatedDatafiles": RELATEDDATAFILE,
    "Rules": RULE,
    "SampleParameters": SAMPLEPARAMETER,
    "SampleTypes": SAMPLETYPE,
    "Samples": SAMPLE,
    "Shifts": SHIFT,
    "Studies": STUDY,
    "StudyInvestigations": STUDYINVESTIGATION,
    "UserGroups": USERGROUP,
    "Users": USER,
}


def type_conversion(python_type):
    """
    Converts python type to openapi param type

    :param python_type: type that is to be converted to flask type
    :return: OpenAPI param spec dict
    """
    if python_type is int:
        return {"type": "integer"}
    if python_type is float:
        return {"type": "number", "format": "float"}
    if python_type is bool:
        return {"type": "boolean"}
    if python_type is datetime.datetime:
        return {"type": "string", "format": "datetime"}
    if python_type is datetime.date:
        return {"type": "string", "format": "date"}
    return {"type": "string"}


def create_entity_models():
    """
    Creates a schema dict for each endpoint

    :return: dict of endpoint names to model
    """
    endpoint_models = {}

    for endpoint in endpoints:
        params = {}
        required = []
        endpoint_inspection = inspect(endpoints[endpoint])
        for column in endpoint_inspection.columns:
            python_type = (
                column.type.impl.python_type
                if hasattr(column.type, "impl")
                else column.type.python_type
            )

            param = type_conversion(python_type)
            if column.name == "ID":
                param["readOnly"] = True
            if column.doc:
                param["description"] = column.doc
            if not column.nullable:
                required.append(column.name)
            params[column.name] = param

        for (
            relationship_name,
            relationship_class,
        ) in endpoint_inspection.relationships.items():
            if (
                relationship_class.direction.name == "MANYTOONE"
                or relationship_class.direction.name == "ONETOONE"
            ):
                params[relationship_name] = {
                    "$ref": f"#/components/schemas/{relationship_name.strip('_')}"
                }
            if (
                relationship_class.direction.name == "MANYTOMANY"
                or relationship_class.direction.name == "ONETOMANY"
            ):
                params[relationship_name] = {
                    "type": "array",
                    "items": {
                        "$ref": f"#/components/schemas/{relationship_name.strip('_')}"
                    },
                }
        endpoint_models[endpoints[endpoint].__name__] = {
            "properties": params,
            "required": required,
        }

    return endpoint_models
