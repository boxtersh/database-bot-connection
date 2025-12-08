from datetime import datetime, date

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


def validate_parameters(command_args, all_id_habits):
    res = None
    if not command_args:
        res = f'Вы не передали ни единого параметра для отметки привычки, повторите ввод'
    elif all_id_habits == set():
        res = f'У вас нет ни одной привычки'
    elif not (id_split:=command_args.split(' ', 1)[0].strip()).isdigit():
        res = f'Вы передали id = {id_split}, что не допустимо, id должно быть положительное целое число. Повторите ввод'
    elif id_split.isdigit():
        if int(id_split) not in all_id_habits:
            res = f'У вас нет привычки c id = {id_split}'
    return res


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
            date_lst = [elem for elem in date_split.split('-')]
            if len(date_lst) == 3 and all(elem.strip().isdigit() for elem in date_lst):
                date_lst = [int(elem.strip()) for elem in date_split.split('-')]
                date_object = date(date_lst[0], date_lst[1], date_lst[2])
                res = f'Указан неверный формат даты, пример допустимой даты: 2013-01-13. Повторите ввод'
                if isinstance(date_object, date):
                    date_ = str(date_object)
                    res = None
            else:
                res = f'Дата пропущена или указан неверный формат даты, пример допустимой даты: 2013-01-13. Повторите ввод'

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