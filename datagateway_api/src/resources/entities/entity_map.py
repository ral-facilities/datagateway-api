import datetime

from sqlalchemy.inspection import inspect

from datagateway_api.common.database.models import EntityHelper


# endpoint_name: entity_name
endpoints = {
    "Applications": "Application",
    "DataCollectionDatafiles": "DataCollectionDatafile",
    "DataCollectionDatasets": "DataCollectionDataset",
    "DataCollectionParameters": "DataCollectionParameter",
    "DataCollections": "DataCollection",
    "DatafileFormats": "DatafileFormat",
    "DatafileParameters": "DatafileParameter",
    "Datafiles": "Datafile",
    "DatasetParameters": "DatasetParameter",
    "DatasetTypes": "DatasetType",
    "Datasets": "Dataset",
    "Facilities": "Facility",
    "FacilityCycles": "FacilityCycle",
    "Groupings": "Grouping",
    "InstrumentScientists": "InstrumentScientist",
    "Instruments": "Instrument",
    "InvestigationGroups": "InvestigationGroup",
    "InvestigationInstruments": "InvestigationInstrument",
    "InvestigationParameters": "InvestigationParameter",
    "InvestigationTypes": "InvestigationType",
    "InvestigationUsers": "InvestigationUser",
    "Investigations": "Investigation",
    "Jobs": "Job",
    "Keywords": "Keyword",
    "ParameterTypes": "ParameterType",
    "PermissibleStringValues": "PermissibleStringValue",
    "PublicSteps": "PublicStep",
    "Publications": "Publication",
    "RelatedDatafiles": "RelatedDatafile",
    "Rules": "Rule",
    "SampleParameters": "SampleParameter",
    "SampleTypes": "SampleType",
    "Samples": "Sample",
    "Shifts": "Shift",
    "Studies": "Study",
    "StudyInvestigations": "StudyInvestigation",
    "UserGroups": "UserGroup",
    "Users": "User",
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
        endpoint_table = EntityHelper.get_entity_object_from_name(endpoints[endpoint])
        endpoint_inspection = inspect(endpoint_table)
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
                    "$ref": f"#/components/schemas/{relationship_name.strip('_')}",
                }
            if (
                relationship_class.direction.name == "MANYTOMANY"
                or relationship_class.direction.name == "ONETOMANY"
            ):
                params[relationship_name] = {
                    "type": "array",
                    "items": {
                        "$ref": f"#/components/schemas/{relationship_name.strip('_')}",
                    },
                }
        endpoint_models[endpoint_table.__name__] = {
            "properties": params,
            "required": required,
        }

    return endpoint_models
