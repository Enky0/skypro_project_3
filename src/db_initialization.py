import os

import psycopg2
from psycopg2 import OperationalError


class DBInit:
    """
    Класс для создания базы данных и таблиц в ней.
    """

    def database_creation(self):
        """
        Метод для создания новой базы данных с названием 'hh_vacancies'
        """

        # на случай, если не удастся установить соединение, чтобы можно было его закрыть без ошибок
        conn = None

        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                database="postgres",
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )

            conn.autocommit = True  # Необходимо для DDL

            with conn.cursor() as cur:
                cur.execute("CREATE DATABASE hh_vacancies")

        except OperationalError as e:
            print(f"Возникло исключение: {e}")
            print("Проверьте, правильно ли введены параметры в файле .env")

        finally:
            if conn is not None:
                conn.close()

    def database_tables_creation(self):
        """
        Метод создает в уже существующей таблице 'hh_vacancies' таблицы: 'employers' и 'vacancies', и колонки к ним
        """

        # на случай, если не удастся установить соединение, чтобы можно было его закрыть без ошибок
        conn = None

        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                database='hh_vacancies',
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )

            conn.autocommit = True

            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS employers (
                employer_id INT PRIMARY KEY,
                employer_name VARCHAR(200) UNIQUE NOT NULL
                )
                """)

                cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id INT PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(employer_id) ON DELETE CASCADE,
                vacancy_name VARCHAR(200) NOT NULL,
                vacancy_salary REAL NOT NULL,
                vacancy_url VARCHAR(200) NOT NULL,
                vacancy_requirements TEXT
                )
                """)

        except OperationalError as e:
            print(f"Возникло исключение: {e}")
            print("Проверьте, правильно ли введены параметры в файле .env")

        finally:
            if conn is not None:
                conn.close()
