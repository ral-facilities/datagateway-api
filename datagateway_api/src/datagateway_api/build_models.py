from datetime import datetime
import logging
from typing import Annotated, List, Optional

from icat.exception import ICATError
from pydantic import BaseModel, create_model, Field

from datagateway_api.src.common.exceptions import PythonICATError
from datagateway_api.src.datagateway_api.icat.helpers import get_cached_client

log = logging.getLogger()


TYPE_MAP = {
    "String": str,
    "Long": int,
    "Date": datetime,
    "Boolean": bool,
    "Double": float,
}

SYSTEM_FIELDS = {
    "id",
    "createId",
    "modId",
    "createTime",
    "modTime",
}


class ICATId(BaseModel):
    id_: int = Field(alias="id")


class ICATBaseEntity(ICATId):
    create_id: str = Field(alias="createId")
    create_time: datetime = Field(alias="createdTime")
    mod_id: str = Field(alias="modId")
    mod_time: datetime = Field(alias="modTime")


def build_datagateway_api_model(**kwargs):
    """
    Build the datagateway models using the SQL scheme given by the ICAT server

    :returns dict of name and pydantic model key value pair
    """
    log.info("Building datagateway models")

    datagateway_api_models = {}

    client_pool = kwargs.get("client_pool")
    client = get_cached_client(None, client_pool)

    try:
        entity_names = client.getEntityNames()
    except ICATError as e:
        raise PythonICATError(e) from e

    for name in entity_names:
        info = client.getEntityInfo(name)
        fields = {}
        post_fields = {}
        patch_fields = {}
        for field in info.fields:
            post_name = f"{name}Post"
            patch_name = f"{name}Patch"
            if field.name in SYSTEM_FIELDS:
                continue

            if field.relType == "ATTRIBUTE":
                field_type = TYPE_MAP.get(field.type, str)
                patch_field_type = Optional[field_type]
                if field.notNullable is False:
                    field_type = Optional[field_type]

                description = getattr(field, "comment", None)
                field_metadata = Field(description=description)
                annotated_type = Annotated[field_type, field_metadata]
                patch_annotated_type = Annotated[patch_field_type, field_metadata]

                field_annotated_type = (
                    (annotated_type, None) if not field.notNullable else annotated_type
                )

                fields[field.name] = field_annotated_type
                post_fields[field.name] = field_annotated_type
                patch_fields[field.name] = (patch_annotated_type, None)

            else:
                rel_model_name = field.type
                post_type = None
                if field.relType == "MANY":
                    rel_type_str = f"List['{rel_model_name}']"  # noqa: B907
                    post_type = List[ICATId]
                else:
                    rel_type_str = f"'{rel_model_name}'"  # noqa: B907
                    post_type = ICATId

                patch_type = Optional[post_type]
                if not field.notNullable:
                    rel_type_str = f"Optional[{rel_type_str}]"
                    post_type = Optional[post_type]

                description = getattr(field, "comment", None)
                field_metadata = Field(description=description)
                annotated_type = Annotated[rel_type_str, field_metadata]
                post_annotated_type = Annotated[post_type, field_metadata]
                patch_annotated_type = Annotated[patch_type, field_metadata]
                fields[field.name] = (
                    (annotated_type, None) if not field.notNullable else annotated_type
                )
                post_fields[field.name] = (
                    (post_annotated_type, None)
                    if not field.notNullable
                    else post_annotated_type
                )
                patch_fields[field.name] = (post_annotated_type, None)

        model = create_model(name, __base__=ICATBaseEntity, **fields)
        post_model = create_model(post_name, **post_fields)
        patch_model = create_model(patch_name, **patch_fields)
        datagateway_api_models[name] = model
        datagateway_api_models[post_name] = post_model
        datagateway_api_models[patch_name] = patch_model

    for model in datagateway_api_models.values():
        model.model_rebuild(_types_namespace=datagateway_api_models)

    log.info("Finished building all datagateway models")
    return datagateway_api_models
