import importlib
import pkgutil
from inspect import isabstract
from typing import Type, Callable, Union


def to_id(value: Union[Type, Callable]):
    return value.__module__ + "." + value.__name__


def import_submodules(package, recursive=True):
    """ Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + '.' + name
        try:
            results[full_name] = importlib.import_module(full_name)
        except ModuleNotFoundError:
            continue
        if recursive and is_pkg:
            results.update(import_submodules(full_name))
    return results


def get_all_subclasses(cls):
    all_subclasses = set()

    for subclass in cls.__subclasses__():
        all_subclasses.add(subclass)
        all_subclasses = all_subclasses.union(get_all_subclasses(subclass))

    return all_subclasses


def get_all_non_abstract_subclasses(cls):
    import_submodules(str(cls.__module__).split('.')[0])
    all_subclasses = get_all_subclasses(cls)
    return [s for s in all_subclasses if not isabstract(s)]
