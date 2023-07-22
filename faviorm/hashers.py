import hashlib
from typing import Iterable

from .ihasher import IHasher


class MD5Hasher(IHasher):
    def hash(self, value: bytes | Iterable[bytes]) -> bytes:
        if isinstance(value, bytes):
            return hashlib.md5(value).digest()
        h = hashlib.md5()
        for v in value:
            h.update(v)
        return h.digest()
