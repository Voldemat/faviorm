from abc import ABC, abstractmethod
from typing import Iterable


class IHasher(ABC):
    @abstractmethod
    def hash(self, value: bytes | Iterable[bytes]) -> bytes:
        pass
