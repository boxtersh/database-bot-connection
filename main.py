import asyncio
import aiogram
from aiogram import filters, F, types
from datetime import date
import token_file as tk
from database import DataBase as DB
from logic import logic_add_habits, validate_parameters, logic_check, Habit, HabitChecks
from dict_query import get_dict_query


bot = aiogram.Bot(token=tk.token())
dp = aiogram.Dispatcher()
db = DB()

@dp.message(filters.Command('start'))
async def start(message: types.Message):
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
        res = (f'Прекрасно, ваша привычка:\n{Habit(name=name, frequency=frequency, created_at=created_at)}'
               f'\nуспешно добавлена 👍')
    await message.reply(res)


@dp.message(filters.Command('list_habits'))
async def list_habits(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    res = await db.list_habits(user_id)
    if res:
        await message.reply(f'Ваши привычки 👇:\n')
        gen_res = ((tuple_[2], tuple_[3], tuple_[4]) for tuple_ in res)
        lst = []
        for name, frequency, created_at in gen_res:
            str_habits = f'{Habit(name=name, frequency=frequency, created_at=created_at)}'
            lst.append(str_habits)
        await message.reply('\n'.join(lst))
    else:
        await message.reply(f'user_id: {user_id}\nУ вас нет ни одной привычки 🤔\n')


@dp.message(filters.Command('check'))
async def list_habits(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    tuple_ = await db.list_id_habits(user_id)
    all_id_habits = {elm for tup in tuple_ for elm in tup}
    res = validate_parameters(command.args, all_id_habits)
    if res is not None:
        await message.reply(res)
        return
    res, habits_id, check_date, note = logic_check(command.args)
    if res is None:
        await db.check(habits_id, check_date, note)
        res = (f'Прекрасно, ваша отметка:\n{HabitChecks(habits_id=habits_id, check_date=check_date, note=note)}'
           f'\nуспешно добавлена 👍')
    await message.reply(res)


# удалить привычку
@dp.message(filters.Command('delete_habit'))
async def delete_habit(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    id = command.args
    tuple_ = await db.list_id_habits(user_id)
    all_id_habits = {elm for tup in tuple_ for elm in tup}
    res = validate_parameters(command.args, all_id_habits)
    if res is None:
        tuple_one = await db.get_habit(id)
        await db.delete_habit(id)
        res = (f'Ваша привычка:\n{Habit(name=tuple_one[2], frequency=tuple_one[3], created_at=tuple_one[4])}'
               f'\nуспешно удалена ❌')
    await message.reply(res)


# удалить отметку
@dp.message(filters.Command('uncheck'))
async def uncheck(message: types.Message, command: filters.CommandObject):
    ...

# Редактировать привычку
@dp.message(filters.Command('edit_habit'))
async def edit_habit(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    tuple_ = await db.list_id_habits(user_id)
    all_id_habits = {elm for tup in tuple_ for elm in tup}
    res = validate_parameters(command.args, all_id_habits)
    if res is None:
        id = command.args.split(' ', 1)[0].strip()
        res = f'{res}\n{id}\n{all_id_habits}'                                                  # Дополнить

    await message.reply(f'{res}')
    # if res is None:
    #     created_at = date.today()
    #     await db.add_habits(user_id, name, frequency, created_at)
    #     res = (f'Прекрасно, ваша привычка:\n{Habit(name=name, frequency=frequency, created_at=created_at)}'
    #            f'\nуспешно изменена 👍')
    # await message.reply(res)

#Получить детали привычки
@dp.message(filters.Command('get_habit'))
async def get_habit(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    tuple_ = await db.list_id_habits(user_id)
    all_id_habits = {elm for tup in tuple_ for elm in tup}
    res = validate_parameters(command.args, all_id_habits)
    if res is None:
        id = command.args.split(' ', 1)[0].strip()
        tuple_one = await db.get_habit(id)
        res = (f'Ваша привычка:\n{Habit(name=tuple_one[2], frequency=tuple_one[3], created_at=tuple_one[4])}')
    await message.reply(f'{res}')


@dp.message(F.text)
async def pay_for_delivery_with_card(message: types.Message):
    await message.reply(f'Вы ввели команду:\n{message.text}\nданная команда мне не известна⁉️ 🤔\n\n'
                        f'Список доступных команд:\n/help\n\n'
                        f'попробуйте ещё раз ✍️, у вас обязательно получится 👇')


async def main():
    await db.creating_tables()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())