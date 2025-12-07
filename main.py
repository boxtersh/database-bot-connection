import asyncio
import aiogram
from aiogram import filters, F, types
from datetime import date
import token_file as tk
from database import DataBase as DB
from logic import logic_add_habits, Habit


bot = aiogram.Bot(token=tk.token())
dp = aiogram.Dispatcher()
db = DB()

@dp.message(filters.Command('start'))
async def start(message: types.Message):
    user_name = message.from_user.username
    await message.reply(f'Приветствую Вас {user_name} 👋, я ваш персональный помощник по созданию привычек, и '
                        f'ведению статистики их выполнения.\nС командами выполнения можете ознакомиться набрав '
                        f'команду /help')


@dp.message(filters.Command('help'))
async def start(message: types.Message):
    await message.reply(f'Список моих доступных команд:\n'
                        f'/start - приветствие, с описанием чат бота;\n'
                        f'/help - список доступных команд;\n'
                        f'/add_habits - добавить привычку, формат:\n'
                        f'/add_habit пить воду | ежедневно;\n'
                        f'/list_habits - посмотреть перечень всех привычек;\n'
                        f'/check 12 - Отметить выполнение сегодня, или\n'
                        f'за указанную дату с комментарием:\n/check 12 2025-12-03 | Выпил 2 л'
                        f'/uncheck - удалить отметку, формат:\n'
                        f'/uncheck 12 2025-12-02;\n'
                        f'/edit_habit - Редактировать привычку, формат:\n'
                        f'/edit_habit 12 Пить воду — немного меньше | еженедельно\n'
                        f'/get_habit - Получить детали привычки, формат:\n'
                        f'/get_habit 12;\n'
                        f'/delete_habit - удаление привычки, формат:\n'
                        f'/delete_habit 12')


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


if __name__ == '__main__':
    asyncio.run(main())