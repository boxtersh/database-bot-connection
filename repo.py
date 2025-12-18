import aiomysql
import asyncio
from dictionary_queries_and_inform import get_dict_query
from config import get_connection_parameters

connection = get_connection_parameters()

class Repo:
    def __init__(self):
        self.host = connection['host']
        self.user = connection['user']
        self.password = connection['password']
        self.database = connection['database']
        self.port = connection['port']
        self.dict_query = get_dict_query()

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
            autocommit=True,
            cursorclass=aiomysql.DictCursor
        )
        return self.connection

    async def creating_tables(self):
        try:
            self.connection = await self.create_connection()
            try:
                async with self.connection.cursor() as cursor:
                    sql_generator = (query.strip() for query in self.dict_query['Создать таблицы в BD'].split(';'))
                    for query in sql_generator:
                        if query:
                            await cursor.execute(query)
            except Exception as err:
                print(f'Ошибка создания таблицы 1{err}')

            self.connection_close()
        except Exception as err:
            print(f'Ошибка связи 2{err}')

    async def add_habits(self, user_id, name, frequency, created_at):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Добавить привычку']
            await cursor.execute(query, [user_id, name, frequency, created_at])
        self.connection_close()

    async def list_habits(self, user_id):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Список привычек']
            await cursor.execute(query, [user_id])
            list_dict_habits = await cursor.fetchall()
            self.connection_close()
            return list_dict_habits

    async def list_id_habits(self, user_id):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Список id привычек']
            await cursor.execute(query, [user_id])
            list_dict_id = await cursor.fetchall()
            self.connection_close()
            return list_dict_id

    async def check (self, habits_id, check_date, note):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Создать отметку']
            await cursor.execute(query, [habits_id, check_date, note])
        self.connection_close()

    async def delete_habit(self, id):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Удалить привычку']
            await cursor.execute(query,[id])
        self.connection_close()

    async def get_all_date_from_habit_checks(self, habits_id) -> set:
        self.connection = await self.create_connection()
        async with (self.connection.cursor() as cursor):
            query = self.dict_query['Все даты отметок']
            await cursor.execute(query, [habits_id])
            list_dictdate = await cursor.fetchall()
        self.connection_close()
        return list_dictdate

    async def get_period_date_from_habit_checks(self, habits_id, beginning, end) -> set:
        self.connection = await self.create_connection()
        async with (self.connection.cursor() as cursor):
            query = self.dict_query['Период дат отметок']
            await cursor.execute(query, [habits_id, beginning, end])
            list_dictdate = await cursor.fetchall()
        self.connection_close()
        return list_dictdate

    async def uncheck(self, habits_id, check_date):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Удалить отметку']
            await cursor.execute(query, [habits_id, check_date])
        self.connection_close()

    async def edit_habit(self, name, frequency, id):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Редактировать привычку']
            await cursor.execute(query, [name, frequency, id])
            self.connection_close()

    async def get_habit(self, id):
        self.connection = await self.create_connection()
        async with self.connection.cursor() as cursor:
            query = self.dict_query['Привычка']
            await cursor.execute(query, [id])
            res = await cursor.fetchone()
            self.connection_close()
            return res


DB = Repo()