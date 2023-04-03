from dataclasses import dataclass
from typing import Any, Generic, List, TypedDict

from app.types.generic import T_MODEL
from app.utils.mixin import SerializableMixin


class ResultWithNbrSerialized(TypedDict):
    total: int
    data: List[Any]


@dataclass
class ResultWithNbr(Generic[T_MODEL], SerializableMixin):
    total: int
    data: List[T_MODEL]

    def serialize(self) -> ResultWithNbrSerialized:
        return ResultWithNbrSerialized(total=self.total, data=[item.serialize() for item in self.data])
