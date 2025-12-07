import asyncio
import aiogram
from aiogram import filters, F, types
from datetime import date
import token_file as tk
from database import DataBase as DB
from logic import logic_add_habits, Habit
from dict_query import get_dict_query


bot = aiogram.Bot(token=tk.token())
dp = aiogram.Dispatcher()
db = DB()

@dp.message(filters.Command('start'))
async def start(message: types.Message):
    user_name = message.from_user.username
    await message.reply(get_dict_query()['Приветствие'])


@dp.message(filters.Command('help'))
async def start(message: types.Message):
    await message.reply(get_dict_query()['Команды'])


@dp.message(filters.Command('add_habits'))
async def add_habits(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    res, name, frequency = logic_add_habits(command.args)
    if res is None:
        created_at = date.today()
        await db.add_habits(user_id, name, frequency, created_at)
        res = (f'Прекрасно, ваша привычка успешно добавлена:\n{Habit(name=name, frequency=frequency, created_at=created_at)}'
               f'user_id: {user_id}\n')
    await message.reply(res)


@dp.message(filters.Command('list_habits'))
async def list_habits(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    res = await db.list_habits(user_id)
    if res:
        await message.reply(f'Ваши привычки 👇:\n')
        for tuple_ in res:
            await message.reply(f'{Habit(name=tuple_[2], frequency=tuple_[3], created_at=tuple_[4])}\n{'*'*5}')
    else:
        await message.reply(f'user_id: {user_id}\nУ вас нет ни одной привычки 🤔\n')


# @dp.message(filters.Command('check'))
# async def list_habits(message: types.Message, command: filters.CommandObject):
#     user_id = message.from_user.id


async def main():
    await dp.start_polling(bot)
    await db.creating_tables()
    print('запуск')

if __name__ == '__main__':
    asyncio.run(main())