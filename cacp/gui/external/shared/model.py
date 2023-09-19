from abc import abstractmethod
from functools import lru_cache
from pydoc import locate
from typing import Type, Dict
from typing import TypeVar, Generic, List

from pydantic import BaseModel

from cacp.gui.external.shared.schema import parse_model
from cacp.gui.external.shared.type import get_all_non_abstract_subclasses, to_id

T = TypeVar("T")

BASE_DATE_FORMAT = "%d/%m/%Y %H:%M:%S"


class BaseAppModel(BaseModel, Generic[T]):

    @classmethod
    @abstractmethod
    def all(cls) -> List[T]:
        return []

    @classmethod
    @abstractmethod
    def get_by_id(cls, _id: str) -> T:
        return None


class ClassModel(BaseAppModel, Generic[T]):
    id: str

    @classmethod
    @abstractmethod
    def from_class(cls, source_class: Type) -> T:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def base_class(cls):
        raise NotImplementedError()

    @property
    def class_type(self) -> Type:
        return locate(self.id)

    @property
    def json_schema(self) -> dict:
        try:
            model: Type[BaseModel] = parse_model(self.class_type)
            schema = model.schema()
            return schema
        except Exception as e:
            print(e)

    @classmethod
    @lru_cache
    def all(cls) -> List[T]:
        return list(cls.all_dict().values())

    @classmethod
    @lru_cache
    def all_dict(cls) -> Dict[str, T]:
        result = {}
        for sub_class in get_all_non_abstract_subclasses(cls.base_class()):
            try:
                model: T = cls.from_class(sub_class)
                model.test()
                _id = to_id(sub_class)
                model.id = _id
                result[_id] = model
            except Exception:
                # do not add those that can not be initialized
                pass
        return result

    @classmethod
    @lru_cache
    def get_by_id(cls, _id: str) -> T:
        return cls.all_dict().get(_id)

    def test(self):
        defaults = {}
        schema = self.json_schema
        for k, v in schema.get("properties").items():
            if default := v.get("default"):
                defaults[k] = default
        self.class_type(**defaults)
