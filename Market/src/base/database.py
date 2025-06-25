import asyncpg


class Database:
    def __init__(self):
        self.connection: asyncpg.Connection = ...


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


class ProjectDatabase(Database):
    def __init__(self):
        super().__init__()


    async def get_catalog(self):
        return await self.execute_get_query("SELECT * FROM catalog")
        
        
    async def get_cb_for_id(self, user_id: int, table: str):
        return await self.execute_get_query(f"SELECT * FROM {table} WHERE id = $1", (user_id,))

        
    async def add_product(self, user_id: int, product_id: int, quantity : int):
        await self.execute_query("INSERT INTO basket(id, product, quantity) VALUES ($1, $2, $3)", (user_id, product_id, quantity,))
    
    
    async def delite_product(self, user_id, product: int):
        await self.execute_query("DELETE FROM basket WHERE id = $1 AND product = $2", (user_id, product,))
    
    
    async def update_product(self, user_id, product_id, amount):
        await self.execute_query("UPDATE basket SET quantity = quantity + $3 WHERE id = $1   AND product = $2 ", (user_id, product_id, amount))
    
    
    
    async def new_user(self, user_id: int, address: int, phone: int):
        await self.execute_query("INSERT INTO users(id, address, phone) VALUES ($1, $2, $3)",
                                 (user_id, address, phone,))
    
    
    async def update_user_info(self, user_id):
        await self.execute_query("UPDATE basket SET pay = $1 WHERE id = $2", (1, user_id))

DATABASE = ProjectDatabase()