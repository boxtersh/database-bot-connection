from aiogram import filters, types, Router
from datetime import date, datetime
import asyncio
from repo import DB
from logic import Habit
from logic import *


router = Router()

# Создание привычки
@router.message(filters.Command('add_habits'))
async def add_habits(message: types.Message, command: filters.CommandObject):
    habit = None
    user_id = message.from_user.id
    res, name, frequency = logic_add_habits(command.args)
    if res is None:
        created_at = date.today()
        await DB.add_habits(user_id, name, frequency, created_at)
        habit = Habit(name=name, frequency=frequency, created_at=created_at)
        res = get_dict_info_for_user()['Привычка добавлена']
    await message.reply(res.format(habit=habit))

# Просмотр списка привычек
@router.message(filters.Command('list_habits'))
async def list_habits(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    username = message.from_user.username
    res = await DB.list_habits(user_id)
    if res:
        res = get_line_habits(res)
    else:
        res = get_dict_info_for_user()['Нет привычек'].format(username=username)
    await message.reply(res)

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
        habit = HabitChecks(habits_id=habits_id, check_date=check_date, note=note)
        res = get_dict_info_for_user()['Отметка добавлена'].format(habit=habit)
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
        habit = Habit(name=tuple_one[2], frequency=tuple_one[3], created_at=tuple_one[4])
        res = get_dict_info_for_user()['Привычка удалена'].format(habit=habit)
    await message.reply(res)


# удалить отметку
@router.message(filters.Command('uncheck'))
async def uncheck(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    tuples = await DB.list_id_habits(user_id)
    res, id, date_ = logic_uncheck(command.args, tuples)
    if res is None:
        tuples_data = await DB.get_all_date_from_habit_checks(id)
        set_date = set_tuples_data(tuples_data)
        if set_date == set():
            res = get_dict_info_for_user()['Нет отметок'].format(id=id)
        elif date_ not in set_date:
            res = get_dict_info_for_user()['Нет отметок на дату'].format(id=id, date_=date_)
        else:
            await DB.uncheck(id, date_)
            res = get_dict_info_for_user()['Отметка удалена'].format(id=id, date_=date_)

    await message.reply(res)


# Редактировать привычку
@router.message(filters.Command('edit_habit'))
async def edit_habit(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    tuples = await DB.list_id_habits(user_id)
    res = validate_parameters(command.args, all_id_habits(tuples))
    if res is None:
        res, name, frequency = validate_name_frequency(command.args)
        if res is None:
            id = get_id_habits(command.args)
            tuple_ = await DB.get_habit(id)
            it_was = f'{Habit(name=tuple_[2], frequency=tuple_[3], created_at=tuple_[4])}'
            it_became = (f'- Название привычки: {name}\n'
                         f'- Частота использования: {frequency}\n'
                         f'- Дата создания: {tuple_[4]}\n')
            await DB.edit_habit(name, frequency, id)
            res = get_dict_info_for_user()['Привычка изменена'].format(it_was=it_was, it_became=it_became)
    await message.reply(res)


# Получить детали привычки
@router.message(filters.Command('get_habit'))
async def get_habit(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    tuples = await DB.list_id_habits(user_id)
    res = validate_parameters(command.args, all_id_habits(tuples))
    if res is None:
        id = get_id_habits(command.args)
        tuple_one = await DB.get_habit(id)
        res = (f'Ваша привычка:\n{Habit(name=tuple_one[2], frequency=tuple_one[3], created_at=tuple_one[4])}')
    await message.reply(f'{res}')


# Получить статистику
@router.message(filters.Command('stats'))
async def get_habit(message: types.Message, command: filters.CommandObject):
    user_id = message.from_user.id
    tuples = await DB.list_id_habits(user_id)
    res = validate_parameters(command.args, all_id_habits(tuples))
    if res is None:
        res, period = argument_in_set_7_30(command.args)
        if res is None:
            id = get_id_habits(command.args)
            habit_object = await DB.get_habit(id)
            begin, end = get_begin_end_period(int(period), habit_object)
            tuples_ = await DB.get_period_date_from_habit_checks(id, begin, end)
            res = logic_stats(tuples_, habit_object, begin, end)
    await message.reply(res)



