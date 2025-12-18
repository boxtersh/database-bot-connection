from datetime import datetime, timedelta

from model import *
from dictionary_queries_and_inform import get_dict_info_for_user


def logic_add_habits(data: str):
    freq = {'ежедневно', 'еженедельно', 'ежемесячно', 'ежегодно', 'произвольно'}
    res = None
    name = None
    frequency = None
    if not data:
        res = get_dict_info_for_user()['Нет частоты']
    elif len(data.split('|')) == 1:
        name = data.split('|')[0].strip()
        frequency = 'произвольно'
    elif len(data.split('|')) == 2 and data.split('|')[1].strip() not in freq and data.split('|')[1].strip() != '':
        res = get_dict_info_for_user()['Неверная частота']
    elif len(data.split('|')) == 2 and data.split('|')[1].strip() not in freq and data.split('|')[1].strip() == '':
        name = data.split('|')[0].strip()
        frequency = 'произвольно'
    elif len(data.split('|')) == 2 and data.split('|')[1].strip() in freq:
        name = data.split('|')[0].strip()
        frequency = data.split('|')[1].strip()
    return res, name, frequency


def get_line_habits(list_dict_habits: list):
    lst = ['Ваши привычки 👇:\n']
    gen_res = ((dict_habits['name'], dict_habits['frequency'], dict_habits['created_at']) for dict_habits in list_dict_habits)
    for name, frequency, created_at in gen_res:
        str_habits = f'{Habit(name=name, frequency=frequency, created_at=created_at)}'
        lst.append(str_habits)
    return '\n'.join(lst)


def all_id_habits(list_dict_id: list):
    return {dict_id['id'] for dict_id in list_dict_id}


def validate_parameters(command_args: str, all_id_habits: set):
    if not command_args:
        return get_dict_info_for_user()['Нет параметров']
    if all_id_habits == set():
        return get_dict_info_for_user()['Нет привычек']
    id = command_args.split(' ', 1)[0].strip()
    if not id.isdigit():
        return get_dict_info_for_user()['Неверный id'].format(id)
    if int(id) not in all_id_habits:
        return f'У вас нет привычки c id = {id}'


def validate_name_frequency(command_args: str):
    name = None
    frequency = None
    res = None
    freq = {'ежедневно', 'еженедельно', 'ежемесячно', 'ежегодно', 'произвольно'}
    split_command_args = command_args.split('|',1)
    if len(split_command_args[0].split(' ', 1)) == 1:
        res = get_dict_info_for_user()['Нет имени привычки']
    elif split_command_args[0].split(' ', 1)[1].strip() == '':
        res = get_dict_info_for_user()['Нет имени привычки']
    elif len(split_command_args) == 1:
        name = split_command_args[0].split(' ', 1)[1].strip()
        frequency = 'произвольно'
    elif len(split_command_args) == 2:
        if split_command_args[1].strip() not in freq and split_command_args[1].strip() == '':
            name = split_command_args[0].split(' ', 1)[1].strip()
            frequency = 'произвольно'
        elif split_command_args[1].strip() in freq and split_command_args[1].strip() != '':
            name = split_command_args[0].split(' ', 1)[1].strip()
            frequency = split_command_args[1].strip()
        else:
            res = get_dict_info_for_user()['Неверная частота ред']
    return res, name, frequency


def attribute_is_date(str_: str):
    res = None
    date_ = None
    len_str_ = len (str_.split(' ', 1))
    if len_str_ != 2:
        res = f'Вы не передали параметр дата в формате: 2013-05-19'
        return res, date_
    if len_str_ == 2:
        date_ = str_.split(' ', 1)[1].strip()[0:10]
        try:
            datetime.strptime(date_, '%Y-%m-%d')
        except ValueError:
            res = get_dict_info_for_user()['Неверная дата'].format(date_=date_)
            date_ = None
        return res, date_


def logic_uncheck(command_args: str, list_dict_id: list):
    id = None
    date_ = None
    res = validate_parameters(command_args, all_id_habits(list_dict_id))
    if res is None:
        id = command_args.split(' ', 1)[0]
        res, date_ = attribute_is_date(command_args)
    return res, id, date_


def logic_check(command_args: str):
    res = None
    id = None
    date_ = None
    note = None
    command_args = command_args.strip()
    list_atrib = command_args.split('|', 1)
    len_atrib = len(list_atrib)

    if len(list_atrib[0].split(' ', 1)) == 1:
        date_ = str(date.today())

    elif len(list_atrib[0].split(' ', 1)) == 2:
        date_split = list_atrib[0].split(' ', 1)[1].strip()
        if not date_split:
            date_ = str(date.today())
        else:
            try:
                datetime.strptime(date_split, '%Y-%m-%d')
                date_ = date_split
                res = None
            except ValueError:
                res = f'Вы передали параметр даты, но такой даты: {date_split} не существует,\nТребуемый формат: 2013-05-19.\nПовторите ввод'

    if len_atrib == 1:
        note = 'Null'
    elif len_atrib == 2:
        note = command_args.split('|', 1)[1].strip()
    else:
        res = f'Недопустимое число параметров. Повторите ввод'

    if command_args.split('|', 1)[0].split()[0].strip().isdigit():
        id = int(command_args.split('|', 1)[0].split()[0].strip())
    else:
        res = f'Неверный формат id, число должно быть целым и положительным. Повторите ввод'

    return res, id, date_, note


def get_id_habits(command_args):
    return int(command_args.split(' ', 1)[0].strip())


def set_tuples_data(list_dictdate):
    return {str(dict_date['check_date']) for dict_date in list_dictdate}


def argument_in_set_7_30(command_args):
    period = {'7', '30'}
    split_args = command_args.split(' ', 1)
    if len(split_args) == 2 and split_args[1].strip().isdecimal() and split_args[1].strip() in period:
        return None, split_args[1].strip()
    res = f'Аргумент статистики 7 или 30 дней не задан\nтребуется формат:\n/stats 12 Х, где Х число 7 или 30\nПовторите ввод'
    return res, None


def get_begin_end_period(period, dict_habit):
    end = date.today()
    begin = end - timedelta(days=period)
    if dict_habit['created_at'] > begin:
        begin = dict_habit['created_at']
    return begin, end


def logic_stats(list_dictdate, dict_habit, begin, end):
    habit = Habit(name=dict_habit['name'], frequency=dict_habit['frequency'], created_at=dict_habit['created_at'])
    frequency = dict_habit['frequency']
    count_checks = len(list_dictdate)
    days_ = (end - begin).days
    res = None
    date_str = ''
    match frequency:
        case 'ежедневно':
            marked  = round(count_checks * 100 / days_,2)
            res = (f'Статистика для привычки:\n{habit} за {days_} дней:\n-выполнено {marked}%\n\n'
                   f'Даты отметок:\n{date_str}')
        case 'еженедельно':
            marked  = round(count_checks * 7 * 100 / (days_),2)
            res = (f'Статистика для привычки:\n{habit} за {days_} дней:\n-выполнено {marked}%\n\n'
                   f'Даты отметок:\n{date_str}')
        case 'ежемесячно':
            marked  = round(count_checks * 30 * 100 / days_, 2)
            res = (f'Статистика для привычки:\n{habit} за {days_} дней:\n-выполнено {marked}%\n\n'
                   f'Даты отметок:\n{date_str}')
        case 'ежегодно':
            marked = round(count_checks * 365 * 100 / days_, 2)
            res = (f'Статистика для привычки:\n{habit} за {days_} дней:\n-выполнено {marked}%\n\n'
                   f'Даты отметок:\n{date_str}')
        case 'произвольно':
            res = f'Для данного периода расчет не производится\n'
    iter_date_str = map(lambda dict_date: str(dict_date['created_at']), list_dictdate)
    date_str = (', ').join(iter_date_str)
    res = res + date_str
    return res