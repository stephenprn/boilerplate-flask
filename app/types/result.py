from dataclasses import dataclass
from typing import Any, Generic, List, TypedDict, TypeVar

from app.models._common import ModelBase
from app.utils.mixin import SerializableMixin

T = TypeVar("T", bound=ModelBase)


class ResultWithNbrSerialized(TypedDict):
    total: int
    data: List[Any]


@dataclass
class ResultWithNbr(Generic[T], SerializableMixin):
    total: int
    data: List[T]

    def serialize(self) -> ResultWithNbrSerialized:
        return ResultWithNbrSerialized(total=self.total, data=[item.serialize() for item in self.data])
