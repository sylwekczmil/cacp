from inspect import isabstract
from typing import Type


def class_to_id(cls: Type):
    return cls.__module__ + '.' + cls.__name__


def get_all_subclasses(cls: Type):
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


def get_all_non_abstract_subclasses(cls):
    all_subclasses = get_all_subclasses(cls)
    return [s for s in all_subclasses if not isabstract(s)]


PRIMITIVE_TYPES = (bool, int, float, complex, str, bool)


def is_primitive_type(thing):
    return thing in PRIMITIVE_TYPES