import asyncpg


class Database:
    def __init__(self):
        self.connection: asyncpg.Connection = ...
        self._last_row_id: int = 0

    async def open_connection(self, host: str, port: int, user: str, password: str, database: str) -> None:
        self.connection = await asyncpg.connect(host=host, port=port, user=user, password=password, database=database)

    async def close_connection(self) -> None:
        if self.connection:
            await self.connection.close()

    async def execute_query(self, query: str, params: tuple = None) -> None:
        async with self.connection.transaction():  # Начать транзакцию
            await self.connection.execute(query, *(params or ()))


    async def execute_get_query(self, query: str, params: tuple = None):
        return await self.connection.fetch(query, *(params or ()))

    @property
    def last_id(self):
        return self._last_row_id


class ProjectDatabase(Database):
    def __init__(self):
        super().__init__()

#####
    async def get_catalog(self):
        return await self.execute_get_query("SELECT * FROM catalog")

    

DATABASE = ProjectDatabase()