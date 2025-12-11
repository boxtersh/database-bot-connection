def get_dict_query():
    dict_query = {'Создать таблицы в BD': """
        SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
        SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
        SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

        CREATE TABLE IF NOT EXISTS habits (
        id BIGINT(9) NOT NULL AUTO_INCREMENT,
        user_id BIGINT(9) NOT NULL,
        name TINYTEXT NOT NULL,
        frequency ENUM('ежедневно', 'еженедельно', 'ежемесячно', 'ежегодно', 'произвольно') NOT NULL DEFAULT 'произвольно',
        created_at DATE NOT NULL,
        PRIMARY KEY (id))
        ENGINE = InnoDB;

        CREATE TABLE IF NOT EXISTS habit_checks (
        id BIGINT(9) NOT NULL AUTO_INCREMENT,
        habits_id BIGINT(9) NOT NULL,
        check_date DATE NOT NULL,
        note VARCHAR(45) NULL DEFAULT 'Null',
        INDEX fk_habit_checks_habits_idx (habits_id ASC),
        PRIMARY KEY (id),
        CONSTRAINT fk_habit_checks_habits
        FOREIGN KEY (habits_id)
        REFERENCES habits (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION)
        ENGINE = InnoDB;

        SET SQL_MODE=@OLD_SQL_MODE;
        SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
        SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
        """,
                  'Добавить привычку':'''INSERT INTO habits (user_id, name, frequency, created_at)
                  VALUES (%s, %s, %s, %s);''',
                  'Список привычек':'SELECT * FROM habits WHERE user_id = %s',
                  'Список id привычек':'SELECT id FROM habits WHERE user_id = %s',
                  'Привычка':'SELECT * FROM habits WHERE id = %s',
                  'Создать отметку':'''INSERT INTO habit_checks (habits_id, check_date, note)
                  VALUES (%s, %s, %s);''',
                  'Удалить привычку':'DELETE FROM habits WHERE id = %s',
                  'Удалить отметку':'DELETE FROM habit_checks WHERE habits_id = %s AND check_date = %s',
                  'Редактировать привычку':'''UPDATE habits
                  SET name = %s, frequency = %s, created_at = %s WHERE id = %s;''',
                  'Привычки пользователя':'SELECT id FROM habits WHERE user_id = %s',
                  'Удалить отметку_инф':'Ваша отметка с id = {id} успешно удалена ❌',
                  'Приветствие':'Приветствую Вас {user_id} 👋, я ваш персональный помощник по созданию привычек, и '
                        f'ведению статистики их выполнения.\nС командами выполнения можете ознакомиться набрав '
                        f'команду /help',
                  'Команды':f'Список моих доступных команд:\n'
                        f'/start - приветствие, с описанием чат бота;\n{'*'*31}\n'
                        f'/help - список доступных команд;\n{'*'*31}\n'
                        f'/add_habits - добавить привычку, формат:\n'
                        f'/add_habit пить воду | ежедневно;\n{'*'*31}\n'
                        f'/list_habits - посмотреть перечень всех привычек;\n{'*'*31}\n'
                        f'/check 12 - Отметить выполнение сегодня, или\n'
                        f'за указанную дату с комментарием:\n/check 12 2025-12-03 | Выпил 2 л\n{'*'*31}\n'
                        f'/uncheck - удалить отметку, формат:\n'
                        f'/uncheck 12 2025-12-02;\n{'*'*31}\n'
                        f'/edit_habit - Редактировать привычку, формат:\n'
                        f'/edit_habit 12 Пить воду — немного меньше | еженедельно\n{'*'*31}\n'
                        f'/get_habit - Получить детали привычки, формат:\n'
                        f'/get_habit 12;\n{'*'*31}\n'
                        f'/delete_habit - удаление привычки, формат:\n'
                        f'/delete_habit 12',
                  }
    return dict_query

