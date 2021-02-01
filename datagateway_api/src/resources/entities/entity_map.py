import datetime

from sqlalchemy.inspection import inspect

from datagateway_api.common.helpers import get_entity_object_from_name
from datagateway_api.src.resources.entities.entity_endpoint_dict import endpoints


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
        endpoint_table = get_entity_object_from_name(endpoints[endpoint])
        endpoint_inspection = inspect(endpoint_table)
        for column in endpoint_inspection.columns:
            # Needed to ensure camelCase field names are used, rather than SNAKE_CASE
            attribute_field_name = endpoint_inspection.get_property_by_column(
                column,
            ).key
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
                required.append(attribute_field_name)
            params[attribute_field_name] = param

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
