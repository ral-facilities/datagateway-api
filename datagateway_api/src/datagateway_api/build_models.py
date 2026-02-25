from datetime import datetime
import logging
from typing import Annotated, List, Optional, Union

from icat.exception import ICATError
from pydantic import BaseModel, create_model, Field

from datagateway_api.src.common.exceptions import PythonICATError
from datagateway_api.src.datagateway_api.icat.helpers import get_cached_client

log = logging.getLogger()


TYPE_MAP = {
    "String": str,
    "Long": int,
    "Date": str,
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
    id_: Annotated[Optional[int], Field(None, alias="id")]


class ICATBaseEntity(ICATId):
    create_id: Annotated[Optional[str], Field(None, alias="createId")]
    create_time: Annotated[Optional[datetime], Field(None, alias="createTime")]
    mod_id: Annotated[Optional[str], Field(None, alias="modId")]
    mod_time: Annotated[Optional[datetime], Field(None, alias="modTime")]


def build_datagateway_api_model(**kwargs):
    """
    Dynamically construct Pydantic models for all ICAT entities exposed by the
    connected ICAT server.

    This function queries the ICAT server for its schema (entity names, fields,
    types, relationships, and nullability) and generates a set of Pydantic
    models representing:

    - The base entity model for each ICAT entity (e.g. `Investigation`)
    - A corresponding POST model for creation (e.g. `InvestigationPost`)
    - A corresponding PATCH model for partial updates (e.g. `InvestigationPatch`)

    Relationship fields (ONE or MANY) are converted into either model references 
    or lists of ICAT IDs. Attribute fields are mapped to Python/Pydantic primitive
    types according to the TYPE_MAP. Optionality and nullability are not strictly
    preserved for all generated fields, as values support the distinct filter 
    operator, which may request one or many values from a given object. Field 
    descriptions from ICAT, when available, are carried over into the model metadata.

    All generated models are finally rebuilt (`model_rebuild`) using the full
    model namespace so that forward references between models resolve correctly.

    Parameters
    ----------
    **kwargs :
        Optional configuration parameters. Expected keys:
        - `client_pool`: A pool or cache of ICAT clients, passed into
          `get_cached_client`.

    Returns
    -------
    dict
        A dictionary mapping model names (e.g. `"Investigation"`,
        `"InvestigationPost"`, `"InvestigationPatch"`) to their corresponding
        dynamically generated Pydantic model classes.

    Raises
    ------
    PythonICATError
        If the ICAT server reports an error while fetching entity names or
        entity schema information.

    Notes
    -----
    - Models include metadata (via `Annotated[... , Field(...)]`) for descriptions.
    - SYSTEM_FIELDS are always excluded from the generated models.
    - Relationship fields use forward references and are resolved at the end of
      generation.
    - The POST and PATCH models differ by optionality and update semantics.

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
        for field in info.fields:
            post_name = f"{name}Post"
            patch_name = f"{name}Patch"
            if field.name in SYSTEM_FIELDS:
                continue

            if field.relType == "ATTRIBUTE":
                field_type = TYPE_MAP.get(field.type, str)
                optional_field_type = Optional[field_type]

                description = getattr(field, "comment", None)
                field_metadata = Field(description=description)
                optional_annotated_type = Annotated[optional_field_type , field_metadata]

                fields[field.name] = (optional_annotated_type, None)
                post_fields[field.name] = (optional_annotated_type, None)

            else:
                rel_model_name = field.type
                post_type = None
                if field.relType == "MANY":
                    rel_type_str = f"List['{rel_model_name}']"  # noqa: B907
                    post_type = f"List['{rel_model_name}Post']"  # noqa: B907
                else:
                    rel_type_str = f"'{rel_model_name}'"  # noqa: B907
                    post_type = Optional[int]

                optional_type = Optional[post_type]
                rel_type_str = f"Optional[{rel_type_str}]"

                description = getattr(field, "comment", None)
                field_metadata = Field(description=description)
                annotated_type = Annotated[rel_type_str, field_metadata]
                optional_annotated_type = Annotated[optional_type, field_metadata]
                fields[field.name] = (annotated_type, None)
                post_fields[field.name] = (optional_annotated_type, None)

        model = create_model(name, __base__=ICATBaseEntity, **fields)
        post_model = create_model(post_name, **post_fields)
        patch_model = create_model(patch_name, __base__=ICATId, **post_fields)
        datagateway_api_models[name] = model
        datagateway_api_models[post_name] = post_model
        datagateway_api_models[patch_name] = patch_model

    for model in datagateway_api_models.values():
        types_namespace = {
            **datagateway_api_models,
            "List": List,
            "Optional": Optional,
            "Union": Union,
        }
        model.model_rebuild(_types_namespace=types_namespace)

    log.info("Finished building all datagateway models")
    return datagateway_api_models
