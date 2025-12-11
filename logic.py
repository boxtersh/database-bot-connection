from datetime import date, datetime
from difflib import restore


class Habit:
    def __init__(self, name: str, frequency: str, created_at: date):
        self.name = name
        self.frequency = frequency
        self.created_at = created_at

    def __str__(self) -> str:
        return (
            f'- Название привычки: {self.name}\n'
            f'- Частота использования: {self.frequency}\n'
            f'- Дата создания: {str(self.created_at)}\n'
        )


class HabitChecks:
    def __init__(self, habits_id: int, check_date: date, note: str):
        self.habits_id = habits_id
        self.check_date = check_date
        self.note = note

    def __str__(self) -> str:
        return (
            f'- id привычки: {self.habits_id}\n'
            f'- Дата отметки: {self.check_date}\n'
            f'- Комментарий: {str(self.note)}\n'
        )


def logic_add_habits(data: str):
    freq = {'ежедневно', 'еженедельно', 'ежемесячно', 'ежегодно', 'произвольно'}
    res = None
    name = None
    frequency = None
    if not data:
        res = f'''Вы не передали параметры частоты привычки в команду /add_habits!
Правильный формат: /add_habits пить воду | X, где Х не указано, либо одно значение из перечня:
ежедневно, еженедельно, ежемесячно, ежегодно, произвольно.
Для не указанного значения частота привычки будет  - произвольно.
Повторите ввод команды'''
    elif len(data.split('|')) == 1:
        name = data.split('|')[0].strip()
        frequency = 'произвольно'
    elif len(data.split('|')) == 2 and data.split('|')[1].strip() not in freq and data.split('|')[1].strip() != '':
        res = f'''Вы передали неверный параметр частоты привычки в команду /add_habits!
Правильный формат: /add_habits пить воду | X, где Х не указано, либо одно значение из перечня:
ежедневно, еженедельно, ежемесячно, ежегодно, произвольно.
Для не указанного значения частота привычки будет  - произвольно.
Повторите ввод команды'''
    elif len(data.split('|')) == 2 and data.split('|')[1].strip() not in freq and data.split('|')[1].strip() == '':
        name = data.split('|')[0].strip()
        frequency = 'произвольно'
    elif len(data.split('|')) == 2 and data.split('|')[1].strip() in freq:
        name = data.split('|')[0].strip()
        frequency = data.split('|')[1].strip()
    return res, name, frequency


def get_line_habits(tuples: tuple):
    lst = ['Ваши привычки 👇:\n']
    gen_res = ((tuple_[2], tuple_[3], tuple_[4]) for tuple_ in tuples)
    for name, frequency, created_at in gen_res:
        str_habits = f'{Habit(name=name, frequency=frequency, created_at=created_at)}'
        lst.append(str_habits)
    return '\n'.join(lst)


def all_id_habits(tuples: tuple):
    return {elm for tuple_ in tuples for elm in tuple_}


def validate_parameters(command_args: str, all_id_habits: set):
    if not command_args:
        return f'Вы не передали ни единого параметра для отметки привычки, повторите ввод'
    if all_id_habits == set():
        return f'У вас нет ни одной привычки'
    id = command_args.split(' ', 1)[0].strip()
    if not id.isdigit():
        return f'Вы передали id = {id}, что не допустимо, id должно быть положительное целое число. Повторите ввод'
    if int(id) not in all_id_habits:
        return f'У вас нет привычки c id = {id}'


def attribute_is_date(str_: str):
    res = None
    date_ = None
    len_str_ = len (str_.split(' ', 1))
    if len_str_ != 2:
        res = f'Вы не передали параметр дата в формате, пример 2013-05-19'
        return res, date_
    if len_str_ == 2:
        date_ = str_.split(' ', 1)[1].strip()
        try:
            datetime.strptime(date_, '%Y-%m-%d')
        except ValueError:
            res = f'Вы передали параметр даты, но такой даты: {date_} не существует,\nТребуемый формат: 2013-05-19.\nПовторите ввод'
            date_ = None
        return res, date_


def logic_uncheck(command_args: str, tuples: tuple):
    id = None
    date_ = None
    res = validate_parameters(command_args, all_id_habits(tuples))
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