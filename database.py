import asyncio
import aiomysql
import dict_query as DQ
import token_file as tk

class DataBase:
    def __init__(self):
        self.host = tk.token()[0]
        self.user = tk.token()[1]
        self.password = tk.token()[2]
        self.database = tk.token()[3]
        self.port = tk.token()[4]
        self.dict_query = DQ.get_dict_query()

    def connection_close(self):
        if self.connection:
            self.connection.close()

    async def create_connection(self):
        self.connection = await aiomysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            db=self.database,
            port=self.port,
            autocommit=True
        )
        return self.connection

    async def creating_tables(self):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            sql_generator = (query.strip() for query in self.dict_query['Создать таблицы в BD'].split(';'))
            for query in sql_generator:
                if query:
                    await cursor.execute(query)

        self.connection_close()

    async def add_habits(self, user_id, name, frequency, created_at):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Добавить привычку']
            await cursor.execute(query, [user_id, name, frequency, created_at])
        self.connection_close()

    async def list_habits(self, user_id):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Лист привычек']
            await cursor.execute(query, [user_id])
            res = await cursor.fetchall()
            self.connection_close()
            return res

    async def check (self, user_id, habits_id, check_date, note):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Создать отметку']
            await cursor.execute(query, [user_id, habits_id, check_date, note])
        self.connection_close()

    async def uncheck(self, user_id, habits_id, check_date):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Удалить отметку']
            await cursor.execute(query, [user_id, habits_id, check_date])
        self.connection_close()

    async def get_data_for_edit_habit(self, id, user_id):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Привычка']
            await cursor.execute(query, [id, user_id])
            res = await cursor.fetchone()
            self.connection_close()
            return res[2], res[3]

    async def edit_habit(self, id, user_id, name, frequency):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Редактировать привычку']
            await cursor.execute(query, [name, frequency, id, user_id])
            self.connection_close()

    async def get_habit(self, id, user_id):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Привычка']
            await cursor.execute(query, [id, user_id])
            res = await cursor.fetchone()
            self.connection_close()
            return res

    async def stats(self, id, user_id):
        res = await self.get_habit(id, user_id)