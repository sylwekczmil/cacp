import uuid
from abc import ABC, abstractmethod
from contextlib import suppress
from dataclasses import dataclass
from functools import lru_cache, cached_property
from inspect import signature, Parameter, isabstract
from pydoc import locate
from typing import (
    Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union, get_args, Callable
)
from typing import Type, get_origin

from pydantic import BaseModel, BaseConfig
from pydantic.fields import ModelField
from river.base import Classifier, DriftDetector, Estimator
from river.datasets.base import Dataset
from river.metrics.base import Metric
from river.optim.base import Initializer, Scheduler, Optimizer

from cacp.gui.external.shared.type import get_all_non_abstract_subclasses, is_primitive_type, to_id

NONE_TYPE = type(None)
SEARCHABLE = [
    Dataset,
    Classifier,
    DriftDetector,
    Optimizer,
    Metric,
    Estimator,
    Initializer,
    Scheduler
]


@dataclass
class ToPydanticMapper(ABC):
    parameter: Parameter

    @abstractmethod
    def can_map(self) -> bool:
        pass

    @abstractmethod
    def map(self) -> ModelField:
        pass

    @cached_property
    def annotation(self):
        args = get_args(self.parameter.annotation)
        if len(args) == 2:
            if args[0] is NONE_TYPE:  # handle type.Optional
                return args[1]
            elif args[1] is NONE_TYPE:  # handle type.Optional
                return args[0]
        return self.parameter.annotation

    @cached_property
    def default(self):
        return self.parameter.default if is_primitive_type(
            self.annotation) and self.parameter.default != self.parameter.empty else None


@dataclass
class SearchableToPydanticMapper(ToPydanticMapper):
    searchable: Optional[Type] = None

    def can_map(self) -> bool:
        annotation = self.annotation
        with suppress(TypeError):
            for searchable in SEARCHABLE:
                if issubclass(annotation, searchable):
                    self.searchable = searchable
                    return True

        return False

    def map(self) -> None:
        # disabled for now, deep level of setup is not required, and is causing recursion
        return None

    @staticmethod
    @lru_cache
    def _searchable_type_to_pseudo_pydantic_model(searchable, annotation):
        model = new_pseudo_pydantic_model(f"{searchable.__name__}__{uuid.uuid4().hex}")
        subclasses = get_all_non_abstract_subclasses(annotation)
        if not subclasses:
            subclasses.append(annotation)
        pseudo_subclasses = [
            new_pseudo_pydantic_model(f"{to_id(x)}__{uuid.uuid4().hex}") for x in
            subclasses
        ]
        p_annotation = Union[tuple(pseudo_subclasses)]
        model.__fields__["option"] = ModelField.infer(
            name="option",
            value=None,
            annotation=p_annotation,
            class_validators=None,
            config=BaseConfig,
        )
        return model


@dataclass
class IterableToPydanticMapper(ToPydanticMapper):
    ITERABLE_TYPES = [
        Deque,
        Dict,
        dict,
        FrozenSet,
        List,
        list,
        Optional,  # Union[x,None]
        Sequence,
        Set,
        set,
        Tuple,
        Union,
    ]

    def can_map(self) -> bool:
        annotation = self.annotation
        origin = get_origin(annotation)
        return origin in self.ITERABLE_TYPES or annotation in self.ITERABLE_TYPES

    def map(self) -> ModelField:
        args = get_args(self.annotation)
        if not args:
            return None
        if len(args) == 1 and args[0] is NONE_TYPE:  # handle type.Optional
            annotation = type_to_pseudo_pydantic_model(args[1], self.parameter.name)
        elif len(args) == 2 and args[1] is NONE_TYPE:  # handle type.Optional
            annotation = type_to_pseudo_pydantic_model(args[0], self.parameter.name)
        else:  # handle other types
            pseudo_values = [type_to_pseudo_pydantic_model(x, self.parameter.name) for x in args]
            annotation = Union[tuple(pseudo_values)]

        return ModelField.infer(
            name=self.parameter.name,
            value=self.default,
            annotation=annotation,
            class_validators=None,
            config=BaseConfig,
        )


@dataclass
class AnyAbstractToPydanticMapper(ToPydanticMapper):

    def can_map(self) -> bool:
        return isabstract(self.annotation)

    def map(self) -> ModelField:
        subclasses = get_all_non_abstract_subclasses(self.annotation)
        pseudo_subclasses = [type_to_pseudo_pydantic_model(x, self.parameter.name) for x in subclasses]
        return ModelField.infer(
            name=self.parameter.name,
            value=self.default,
            annotation=Union[tuple(pseudo_subclasses)],
            class_validators=None,
            config=BaseConfig,
        )


@dataclass
class AnyToPydanticMapper(ToPydanticMapper):

    def can_map(self) -> bool:
        if "typing.Callable" in str(self.annotation):
            return False
        return True

    def map(self) -> ModelField:
        annotation = type_to_pseudo_pydantic_model(self.annotation, self.parameter.name)
        return ModelField.infer(
            name=self.parameter.name,
            value=self.default,
            annotation=annotation,
            class_validators=None,
            config=BaseConfig,
        )


@dataclass
class DocToPydanticMapper:

    @classmethod
    def map(cls, class_type, parameter) -> ModelField:
        doc_string = class_type.__doc__
        if doc_string:
            parameter_in_doc_string = f"{parameter.name} :"
            for l in doc_string.split("\n"):
                l = l.strip()
                if l.startswith(parameter_in_doc_string):
                    possible_primitive = l.replace(parameter_in_doc_string, "").strip().split(",")[0]
                    if possible_primitive in ["bool", "int", "float", "str"]:
                        return ModelField.infer(
                            name=parameter.name,
                            value=None,
                            annotation=locate(possible_primitive),
                            class_validators=None,
                            config=BaseConfig,
                        )


MAPPER_CLASSES = [
    SearchableToPydanticMapper,
    IterableToPydanticMapper,
    AnyAbstractToPydanticMapper,
    AnyToPydanticMapper
]


def new_pseudo_pydantic_model(name: str):
    class Model(BaseModel):
        pass

    Model.__name__ = name
    return Model


@lru_cache
def function_to_pseudo_pydantic_model(function: Callable):
    model = new_pseudo_pydantic_model(function.__name__)
    sig = signature(function)
    parameters: List[Parameter] = list(sig.parameters.values())
    for parameter in parameters:
        if parameter.annotation == parameter.empty and parameter.default != parameter.empty:
            potential_annotation_type = type(parameter.default)
            if is_primitive_type(potential_annotation_type):
                parameter._annotation = potential_annotation_type
        if parameter.annotation != parameter.empty:
            for mapper_class in MAPPER_CLASSES:
                mapper = mapper_class(parameter)
                if mapper.can_map():
                    field = mapper.map()
                    if field:
                        model.__fields__[parameter.name] = field
                    break
        else:
            field = DocToPydanticMapper.map(function, parameter)
            if field:
                model.__fields__[parameter.name] = field
    return model


@lru_cache
def type_to_pseudo_pydantic_model(t: Type, alternative_name: str = None):
    if is_primitive_type(t):
        return t

    model = new_pseudo_pydantic_model(t.__name__ if hasattr(t, "__name__") else alternative_name)
    sig = signature(t.__init__)
    init_parameters: List[Parameter] = list(sig.parameters.values())[1:]
    for parameter in init_parameters:
        if parameter.annotation == parameter.empty and parameter.default != parameter.empty:
            potential_annotation_type = type(parameter.default)
            if is_primitive_type(potential_annotation_type):
                parameter._annotation = potential_annotation_type
        if parameter.annotation != parameter.empty:
            for mapper_class in MAPPER_CLASSES:
                mapper = mapper_class(parameter)
                if mapper.can_map():
                    field = mapper.map()
                    if field:
                        model.__fields__[parameter.name] = field
                    break
        else:
            field = DocToPydanticMapper.map(t, parameter)
            if field:
                model.__fields__[parameter.name] = field

    return model
