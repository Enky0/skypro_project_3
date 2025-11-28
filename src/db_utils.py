import os

import psycopg2
from psycopg2 import OperationalError


class DBChecker:
    """
    Вспомогательный класс, содержащий методы проверки существования базы данных, и необходимых таблиц в ней
    """

    def check_db_exists(self) -> bool:
        """
        Метод проверяет, существует ли уже база данных.
        :return: True/False
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

            with conn.cursor() as cur:
                cur.execute("SELECT 1 FROM pg_database WHERE datname = 'hh_vacancies'")
                return bool(cur.fetchone())

        except OperationalError as e:
            print(f"Возникло исключение: {e}")
            print("Проверьте, правильно ли введены параметры в файле .env")

        finally:
            if conn is not None:
                conn.close()

    def check_db_tables_exist(self) -> bool:
        """
        Метод проверяет, существуют ли необходимые таблицы в базе данных
        :return: True / False
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

            with conn.cursor() as cur:
                query = """
                SELECT EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = %s
                AND table_name = 'employers'
                ),
                EXISTS (
                SELECT 1 FROM information_schema.tables
                WHERE table_schema = %s
                AND table_name = 'vacancies'
                )
                """

                cur.execute(query, ('public', 'public'))

                # возвращает True, если обе таблицы существуют
                table_employer_exists, table_vacancies_exists = cur.fetchone()

            return table_employer_exists and table_vacancies_exists

        except OperationalError as e:
            print(f"Возникло исключение: {e}")
            print("Проверьте, правильно ли введены параметры в файле .env")

        finally:
            if conn is not None:
                conn.close()


class DBDataCleaner():
    """
    Класс для очистки данных в таблицах БД
    """
    def clean_all_data(self):
        """
        Метод очищает все данные из таблиц employers и vacancies
        """
        conn = None

        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST'),
                database='hh_vacancies',
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD')
            )

            with conn.cursor() as cur:
                cur.execute("TRUNCATE TABLE vacancies, employers CASCADE")
                conn.commit()

        except OperationalError as e:
            print(f"Возникло исключение: {e}")
            print("Проверьте, правильно ли введены параметры в файле .env")

        finally:
            if conn is not None:
                conn.close()
