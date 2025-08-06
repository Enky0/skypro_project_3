import os

import psycopg2
from psycopg2 import OperationalError


class DBFiller:
    """
    Класс для заполнения таблиц базы данных
    """

    def __init__(self):
        pass

    def db_data_fill(self, vacancies_list: list[dict]):
        """
        Метод заполняет таблицы в базе данных
        :param vacancies_list: список вакансий полученный с API hh.ru
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
                for vacancy in vacancies_list:
                    cur.execute("""
                    INSERT INTO employers (employer_id, employer_name)
                    VALUES (%s, %s)
                    ON CONFLICT (employer_id) DO NOTHING
                    """, (vacancy["employer_id"], vacancy["employer_name"]))

                    cur.execute("""
                    INSERT INTO vacancies (
                    vacancy_id,
                    employer_id,
                    vacancy_name,
                    vacancy_requirements,
                    vacancy_salary,
                    vacancy_url
                    )
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (vacancy_id)
                    DO NOTHING
                    """, (vacancy["vacancy_id"], vacancy["employer_id"], vacancy["vacancy_name"],
                          vacancy["vacancy_requirements"], vacancy["vacancy_salary"], vacancy["vacancy_url"]))

                    conn.commit()

        except OperationalError as e:
            print(f"Возникло исключение: {e}")
            print("Проверьте, правильно ли введены параметры в файле .env")
            if conn:
                conn.rollback()

        except Exception as e:
            print(f"Неизвестная ошибка: {e}")
            if conn:
                conn.rollback()

        finally:
            if conn is not None:
                conn.close()
