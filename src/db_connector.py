import os

import psycopg2
from psycopg2 import OperationalError


class DBManager:
    """
    Класс взаимодействующий с базой данных.
    Методы только выводят информацию из БД.
    """

    def get_companies_and_vacancies_count(self) -> list[tuple]:
        """
        Метод возвращает список всех компаний, и количество вакансий у каждой компании.
        """
        query = """
        SELECT employer_name, COUNT(*) AS vacancy_count
        FROM employers
        JOIN vacancies ON employers.employer_id = vacancies.employer_id
        GROUP BY employer_name
        ORDER BY vacancy_count DESC;
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
                cur.execute(query)
                result = cur.fetchall()
            return result

        except OperationalError as e:
            print(f"Возникло исключение: {e}")
            print("Проверьте, правильно ли введены параметры в файле .env")

        finally:
            if conn is not None:
                conn.close()

    def get_all_vacancies(self) -> list[tuple]:
        """
        Метод возвращает список всех вакансий с указанием названия компании,
        названия вакансии, зарплаты, и ссылки на вакансию.
        """
        query = """
        SELECT employers.employer_name, vacancies.vacancy_name, vacancies.vacancy_salary, vacancies.vacancy_url
        FROM vacancies
        JOIN employers ON employers.employer_id = vacancies.employer_id
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
                cur.execute(query)
                result = cur.fetchall()
            return result

        except OperationalError as e:
            print(f"Возникло исключение: {e}")
            print("Проверьте, правильно ли введены параметры в файле .env")

        finally:
            if conn is not None:
                conn.close()

    def get_avg_salary(self) -> list[tuple]:
        """
        Метод возвращает среднюю зарплату по вакансиям.
        """
        query = """
        SELECT AVG(vacancy_salary) AS avg_salary
        FROM vacancies
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
                cur.execute(query)
                result = cur.fetchall()
            return result

        except OperationalError as e:
            print(f"Возникло исключение: {e}")
            print("Проверьте, правильно ли введены параметры в файле .env")

        finally:
            if conn is not None:
                conn.close()

    def get_vacancies_with_higher_salary(self) -> list[tuple]:
        """
        Метод возвращает список всех вакансий, у которых зарплата выше средней по всем вакансиям.
        """
        query = """
        SELECT employers.employer_name, vacancies.vacancy_name, vacancies.vacancy_salary, vacancies.vacancy_url,
        vacancies.vacancy_requirements
        FROM vacancies
        JOIN
        employers ON vacancies.employer_id = employers.employer_id
        WHERE vacancy_salary > (SELECT AVG(vacancy_salary) FROM vacancies)
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
                cur.execute(query)
                result = cur.fetchall()
            return result

        except OperationalError as e:
            print(f"Возникло исключение: {e}")
            print("Проверьте, правильно ли введены параметры в файле .env")

        finally:
            if conn is not None:
                conn.close()

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple]:
        """
        Метод возвращает список всех вакансий, в названии которых содержатся переданные в метод слова.
        """
        query = """
        SELECT employers.employer_name, vacancies.vacancy_name, vacancies.vacancy_salary, vacancies.vacancy_url,
        vacancies.vacancy_requirements
        FROM vacancies
        JOIN
        employers ON vacancies.employer_id = employers.employer_id
        WHERE vacancy_name LIKE %s
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
                cur.execute(query, (f"%{keyword}%",))
                result = cur.fetchall()
            return result

        except OperationalError as e:
            print(f"Возникло исключение: {e}")
            print("Проверьте, правильно ли введены параметры в файле .env")

        finally:
            if conn is not None:
                conn.close()
