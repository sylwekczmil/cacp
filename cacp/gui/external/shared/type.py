from inspect import isabstract
from typing import Type, Callable, Union


def to_id(value: Union[Type, Callable]):
    return value.__module__ + "." + value.__name__


def get_all_subclasses(cls: Type):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


def get_all_non_abstract_subclasses(cls):
    all_subclasses = get_all_subclasses(cls)
    return [s for s in all_subclasses if not isabstract(s)]


PRIMITIVE_TYPES = (bool, int, float, complex, str)


def is_primitive_type(thing):
    return thing in PRIMITIVE_TYPES
