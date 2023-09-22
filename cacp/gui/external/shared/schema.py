from __future__ import annotations

from functools import lru_cache
from inspect import signature
from pydoc import locate
from typing import Type, get_type_hints

from pydantic import BaseModel, BaseConfig
from pydantic.fields import ModelField


def _new_pseudo_pydantic_model(name: str) -> Type[BaseModel]:
    class Model(BaseModel):
        pass

    Model.__name__ = name
    return Model


@lru_cache
def _try_parse(field_name: str, field_type_hint, default_value):
    try:
        field = ModelField.infer(
            name=field_name,
            value=default_value,
            annotation=field_type_hint,
            class_validators=None,
            config=BaseConfig,
        )
        model = _new_pseudo_pydantic_model("test")
        model.__fields__[field_name] = field
        model.schema()
        return field
    except Exception:
        return None


def _try_parse_doc(field_name: str, class_type: Type, default_value):
    doc_string = class_type.__doc__
    if doc_string:
        parameter_in_doc_string = f"{field_name} :"
        for line in doc_string.split("\n"):
            line = line.strip()
            if line.startswith(parameter_in_doc_string):
                possible_primitive = line.replace(parameter_in_doc_string, "").strip().split(",")[0]
                if possible_primitive in ["bool", "int", "float", "str"]:
                    return _try_parse(field_name, locate(possible_primitive), default_value)


def parse_model(t: Type) -> Type[BaseModel]:
    model = _new_pseudo_pydantic_model(t.__name__)
    init_signature = signature(t.__init__)
    init_type_hints = get_type_hints(t.__init__)
    init_parameters = init_signature.parameters

    for field_name in init_parameters:
        field_parameter = init_parameters[field_name]
        default_value = field_parameter.default if field_parameter.default != field_parameter.empty else None
        field_type_hint = init_type_hints.get(field_name)
        if field_type_hint:
            if field := _try_parse(field_name, field_type_hint, default_value):
                model.__fields__[field_name] = field
        else:
            if field := _try_parse_doc(field_name, t, default_value):
                model.__fields__[field_name] = field

    return model
