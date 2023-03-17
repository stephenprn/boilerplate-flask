from abc import ABC, abstractmethod
from typing import Dict


class SerializableMixin(ABC):
    @abstractmethod
    def serialize(self, *args, **kwargs) -> Dict:
        raise NotImplementedError
