import os

import asyncpg

from faviorm.executors import AsyncPgSQLLoaderExecutor


async def test_asyncpg_executor() -> None:
    executor = AsyncPgSQLLoaderExecutor(asyncpg=asyncpg)
    await executor.init(
        host=os.environ["POSTGRES_HOST"],
        port=int(os.environ["POSTGRES_PORT"]),
        username=os.environ["POSTGRES_USER"],
        password=os.environ.get("POSTGRES_PASSWORD", None),
        database=os.environ["POSTGRES_DB"],
    )
    try:
        result = await executor.execute("SELECT 1;")
        assert len(result) == 1
        assert result[0][0] == 1
    finally:
        await executor.teardown()
