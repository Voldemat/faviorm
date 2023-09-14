from typing import Any, Protocol, Sequence, TYPE_CHECKING

if TYPE_CHECKING:
    try:
        from asyncpg import Connection, Record
    except ImportError:
        pass
from ..iloader import ISQLLoaderExecutor, ISQLQueryResult


class AsyncPgModuleProtocol(Protocol):
    async def connect(
        self,
        *,
        host: str,
        port: int,
        user: str,
        database: str,
        password: str | None,
    ) -> "Connection[Record]":
        pass


class AsyncPgSQLLoaderExecutor(ISQLLoaderExecutor):
    asyncpg: AsyncPgModuleProtocol
    _conn: "Connection[Record] | None"

    def __init__(self, asyncpg: AsyncPgModuleProtocol) -> None:
        self.asyncpg = asyncpg
        self._conn = None

    @property
    def conn(self) -> "Connection[Record]":
        if self._conn is None:
            raise ValueError("Loader is not initialized yet")
        return self._conn

    async def init(
        self,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str | None,
        **kwargs: Any,
    ) -> None:
        self._conn = await self.asyncpg.connect(
            host=host,
            port=port,
            database=database,
            user=username,
            password=password,
            **kwargs,
        )

    async def execute(
        self, query: str, args: Sequence[Any] = [], **kwargs: Any
    ) -> list[ISQLQueryResult]:
        return await self.conn.fetch(  # type: ignore [no-any-return]
            query, *args, **kwargs
        )

    async def teardown(self, timeout_s: float = 5) -> None:
        if self._conn is None:
            raise ValueError("Loader is not initialized to perform teardown")
        await self._conn.close(timeout=timeout_s)
        self._conn = None
