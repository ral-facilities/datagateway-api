from typing import Annotated

from pydantic import BaseModel, create_model, Field


def make_fields_optional(model_cls: type[BaseModel]) -> type[BaseModel]:
    new_fields = {}

    for f_name, f_info in model_cls.model_fields.items():
        f_dct = f_info.asdict()
        new_fields[f_name] = (
            Annotated[f_dct["annotation"] | None, *f_dct["metadata"], Field(**f_dct["attributes"])],
            None,
        )

    return create_model(
        f"{type.__name__}Optional",
        __base__=model_cls,
        **new_fields,
    )
