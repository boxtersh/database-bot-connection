from aiogram import filters, types, Router
from repo import DB
from dictionary_queries_and_inform import get_dict_query
from logic import *


router = Router()

# Создание привычки
@router.message(filters.Command('add_habits'))
async def add_habits(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    res, name, frequency = logic_add_habits(command.args)
    if res is None:
        created_at = date.today()
        await DB.add_habits(user_id, name, frequency, created_at)
        res = (f'Прекрасно, ваша привычка:\n{Habit(name=name, frequency=frequency, created_at=created_at)}'
               f'\nуспешно добавлена 👍')
    await message.reply(res)

# Просмотр списка привычек
@router.message(filters.Command('list_habits'))
async def list_habits(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    res = await DB.list_habits(user_id)
    if res:
        await message.reply(get_line_habits(res))
    else:
        await message.reply(f'user_id: {user_id}\nУ вас нет ни одной привычки 🤔\n')

# Отметить выполнение привычки
@router.message(filters.Command('check'))
async def list_habits(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    tuples = await DB.list_id_habits(user_id)
    res = validate_parameters(command.args, all_id_habits(tuples))
    if res is not None:
        await message.reply(res)
        return
    res, habits_id, check_date, note = logic_check(command.args)
    if res is None:
        await DB.check(habits_id, check_date, note)
        res = (f'Прекрасно, ваша отметка:\n{HabitChecks(habits_id=habits_id, check_date=check_date, note=note)}'
           f'\nуспешно добавлена 👍')
    await message.reply(res)


# удалить привычку
@router.message(filters.Command('delete_habit'))
async def delete_habit(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    id = command.args
    tuples = await DB.list_id_habits(user_id)
    res = validate_parameters(command.args, all_id_habits(tuples))
    if res is None:
        tuple_one = await DB.get_habit(id)
        await DB.delete_habit(id)
        res = (f'Ваша привычка:\n{Habit(name=tuple_one[2], frequency=tuple_one[3], created_at=tuple_one[4])}'
               f'\nуспешно удалена ❌')
    await message.reply(res)


# удалить отметку
@router.message(filters.Command('uncheck'))
async def uncheck(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    tuples = await DB.list_id_habits(user_id)
    res, id, date_ = logic_uncheck(command.args, tuples)
    if res is None:
        await DB.uncheck(id, date_)
        res = get_dict_query()['Удалить отметку_инф'].format(id=id)
    await message.reply(res)


# ❌Редактировать привычку
@router.message(filters.Command('edit_habit'))
async def edit_habit(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    tuples = await DB.list_id_habits(user_id)
    res = validate_parameters(command.args, all_id_habits(tuples))
    if res is None:
        id = command.args.split(' ', 1)[0].strip()
        res = f'{res}\n{id}\n{all_id_habits}'                                                  # Дополнить

    await message.reply(f'{res}')
    # if res is None:
    #     created_at = date.today()
    #     await DB.add_habits(user_id, name, frequency, created_at)
    #     res = (f'Прекрасно, ваша привычка:\n{Habit(name=name, frequency=frequency, created_at=created_at)}'
    #            f'\nуспешно изменена 👍')
    # await message.reply(res)
    ...

# Получить детали привычки
@router.message(filters.Command('get_habit'))
async def get_habit(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    tuples = await DB.list_id_habits(user_id)
    res = validate_parameters(command.args, all_id_habits(tuples))
    if res is None:
        id = command.args.split(' ', 1)[0].strip()
        tuple_one = await DB.get_habit(id)
        res = (f'Ваша привычка:\n{Habit(name=tuple_one[2], frequency=tuple_one[3], created_at=tuple_one[4])}')
    await message.reply(f'{res}')


# ❌ Получить статистику
@router.message(filters.Command('stats'))
async def get_habit(message: types.Message, command: filters.CommandObject):
    ...



