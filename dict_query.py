def get_dict_query():
    dict_query = {'Создать таблицы в BD': """
        SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
        SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
        SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

        CREATE TABLE IF NOT EXISTS habits (
        id BIGINT(9) NOT NULL AUTO_INCREMENT,
        user_id INT NOT NULL,
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
        REFERENCES seschool_01_RP12_TYA.habits (id)
        ON DELETE CASCADE
        ON UPDATE NO ACTION)
        ENGINE = InnoDB;

        SET SQL_MODE=@OLD_SQL_MODE;
        SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
        SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
        """,
                  'Добавить привычку':'''INSERT INTO habits (user_id, name, frequency, created_at)
                  VALUES (%s, %s, %s, %s);''',
                  'Лист привычек':'SELECT * FROM habits WHERE user_id = %s',
                  'Привычка':'SELECT * FROM habits WHERE id = %s AND user_id = %s',
                  'Создать отметку':'''INSERT INTO habit_checks (user_id, habits_id, check_date, note)
                  VALUES (%s, %s, %s, %s);''',
                  'Удалить отметку':'DELETE FROM habit_checks WHERE user_id = %s AND habits_id = %s AND check_date = %s',
                  'Редактировать привычку':'''UPDATE habits
                  SET name = %s, frequency = %s WHERE id = %s AND user_id = %s;''',
                  }
    return dict_query