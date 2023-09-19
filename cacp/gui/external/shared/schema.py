from __future__ import annotations

from functools import lru_cache
from inspect import signature
from typing import Type, get_type_hints

from pydantic import BaseModel, BaseConfig
from pydantic.fields import ModelField


def _new_pseudo_pydantic_model(name: str):
    class Model(BaseModel):
        pass

    Model.__name__ = name
    return Model


@lru_cache
def _try_parse(field_name: str, field_type_hint: Type, default_value):
    model = _new_pseudo_pydantic_model("test")
    try:
        field = ModelField.infer(
            name=field_name,
            value=default_value,
            annotation=field_type_hint,
            class_validators=None,
            config=BaseConfig,
        )
        model.__fields__[field_name] = field
        model.schema()
        return field
    except Exception:
        return None


def parse_model(t: Type) -> Type[bool | int | float | complex | str | BaseModel, None]:
    model = _new_pseudo_pydantic_model(t.__name__)
    init_signature = signature(t.__init__)
    init_type_hints = get_type_hints(t.__init__)
    init_parameters = init_signature.parameters
    for field_name, field_type_hint in init_type_hints.items():
        field_parameter = init_parameters[field_name]
        default_value = field_parameter.default if field_parameter.default != field_parameter.empty else None
        if field := _try_parse(field_name, field_type_hint, default_value):
            model.__fields__[field_name] = field
    return model
