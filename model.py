from dataclasses import dataclass
from datetime import date


@dataclass
class Habit:
        name: str
        frequency: str='произвольно'
        created_at: date = date.today()

        def __str__(self) -> str:
            return (
                f'- Название привычки: {self.name}\n'
                f'- Частота использования: {self.frequency}\n'
                f'- Дата создания: {str(self.created_at)}\n'
            )


@dataclass
class HabitChecks:
        habits_id: int
        check_date: date = date.today()
        note: str = 'Null'

        def __str__(self) -> str:
            return (
                f'- id привычки: {self.habits_id}\n'
                f'- Дата отметки: {self.check_date}\n'
                f'- Комментарий: {str(self.note)}\n'
            )