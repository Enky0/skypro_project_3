from src.db_connector import DBManager
from src.db_initialization import DBInit
from src.db_table_filler import DBFiller
from src.db_utils import DBChecker, DBDataCleaner
from src.hh import HH
from src.utils import EnvFileChecker
from src.vacancies import Vacancy
from src.vacancies_filter import VacancyFilter


class UserInteraction:
    """
    Класс для взаимодействия с пользователем
    """

    @staticmethod
    def interaction_with_user() -> None:
        """
        Метод для взаимодействия с пользователем
        """
        # взаимодействие с классом EnvFileChecker
        env_checker_object = EnvFileChecker()
        if not env_checker_object():
            print("Отсутствует файл .env или он не заполнен")
            return None

        while True:  # запрос у пользователя ключевого слова для поиска вакансий
            user_input_word_for_vacancy_search = input("По какому слову произвести поиск вакансий? ")
            if not user_input_word_for_vacancy_search.strip():
                print("Ошибка: Слово для поиска не должно быть пустым")
                continue
            else:
                break

        # взаимодействие с классом HH
        hh_object = HH()

        hh_search_result = hh_object(user_input_word_for_vacancy_search)

        # взаимодействие с классами VacancyFilter и Vacancy
        if hh_search_result:
            vacancy_filter_object = VacancyFilter(hh_search_result)
            top_employers_vacancies = vacancy_filter_object.get_vacancies_by_top_employers()

            vacancy_object = Vacancy(top_employers_vacancies)
            filtered_vacancies = vacancy_object.get_vacancies()

        else:
            print("Ошибка! Поиск по вакансиям не удался: API ничего не вернул.")
            return None

        # взаимодействие с классами DBChecker и DBInit
        db_checker_object = DBChecker()

        # создание базы данных с таблицами
        if not db_checker_object.check_db_exists():
            db_init_object = DBInit()
            db_init_object.database_creation()
            db_init_object.database_tables_creation()
        else:
            db_init_object = DBInit()
            db_init_object.database_tables_creation()  # создание таблиц, если отсутствуют

        # взаимодействие с классом DBFiller

        db_filler_object = DBFiller()
        db_filler_object.db_data_fill(filtered_vacancies)

        # взаимодействие с классом DBManager

        db_manager_object = DBManager()

        while True:
            user_response = input(
                "Выберите номер действия: "
                "[1. Вывести список всех компаний, и количество вакансий у каждой. "
                "2. Вывести список всех вакансий с информацией. "
                "3. Вывести список всех вакансий, у которых зарплата выше средней по всем вакансиям. "
                "4. Провести поиск всех вакансий по ключевому слову. "
                "5. Системные функции. "
                "6. Завершить выполнение программы.] ")

            # Все компании и количество их вакансий
            if user_response == "1":
                employers_vacancies_list = db_manager_object.get_companies_and_vacancies_count()
                for company, count in employers_vacancies_list:
                    print(f"{company}: {count} вакансий")
                continue

            # Все вакансии с информацией
            if user_response == "2":
                all_vacancies_info = db_manager_object.get_all_vacancies()
                vacancy_counter = 1
                for company, vacancy, salary, url in all_vacancies_info:
                    console_message = \
                        f"""
                        Вакансия №{vacancy_counter}:
                        Компания-работодатель: {company}
                        Название вакансии: {vacancy}
                        Минимальная зарплата: {salary}
                        Ссылка на вакансию: {url}
"""
                    print(console_message)
                    vacancy_counter += 1
                continue

            # Все вакансии с зарплатой выше средней по всем вакансиям
            if user_response == "3":
                above_avg_salary_vacancies = db_manager_object.get_vacancies_with_higher_salary()
                vacancy_counter = 1
                for company, vacancy, salary, url, requirements in above_avg_salary_vacancies:
                    console_message = \
                        f"""
                        Вакансия №{vacancy_counter}:
                        Компания-работодатель: {company}
                        Название вакансии: {vacancy}
                        Минимальная зарплата: {salary}
                        Ссылка на вакансию: {url}
                        Требования вакансии: {requirements}
                """
                    print(console_message)
                    vacancy_counter += 1
                continue

            # Поиск всех вакансий по ключевому слову
            if user_response == "4":
                while True:
                    user_keyword = input("Введите ключевое слово для поиска ")
                    if not user_keyword.strip:
                        print("Ошибка: нельзя вводить пустой запрос")
                        continue
                    vacancies_with_keyword = db_manager_object.get_vacancies_with_keyword(user_keyword)
                    if not vacancies_with_keyword:
                        while True:
                            user_response = input(
                                "Не найдено ни одной вакансии с этим ключевым словом, попробовать еще раз? "
                                "[1. Да. "
                                "2. Нет.] ")
                            if user_response in ["1", "2"]:
                                break
                            else:
                                print("Ошибка: Неизвестный ответ. Выберите 1 или 2")
                                continue
                        if user_response == "1":
                            continue
                        if user_response == "2":
                            break
                    else:
                        vacancy_counter = 1
                        for company, vacancy, salary, url, requirements in vacancies_with_keyword:
                            console_message = \
                                f"""
                                Вакансия №{vacancy_counter}:
                                Компания-работодатель: {company}
                                Название вакансии: {vacancy}
                                Минимальная зарплата: {salary}
                                Ссылка на вакансию: {url}
                                Требования вакансии: {requirements}
"""
                            print(console_message)
                            vacancy_counter += 1
                    break
                continue

            # Удаление данных из таблицы
            if user_response == "5":
                while True:
                    user_response = input(
                        "Выберите номер действия: "
                        "[1. Очистить данные из таблиц. "
                        "2. Отмена.] ")
                    if user_response in ["1", "2"]:
                        break
                    else:
                        print("Ошибка: Неизвестный ответ. Выберите 1 или 2.")
                        continue

                # Подтверждение удаления данные + удаление данных с завершением выполнения программы
                if user_response == "1":
                    while True:
                        user_response = input(
                            "Внимание, все данные из таблиц будут очищены, и после этого выполнение программы "
                            "завершится, продолжить? "
                            "[1. Продолжить. "
                            "2. Отмена.] ")
                        if user_response in ["1", "2"]:
                            break
                        else:
                            print("Ошибка: Неизвестный ответ. Выберите 1 или 2.")
                            continue
                    if user_response == "1":
                        data_cleaner_object = DBDataCleaner()
                        data_cleaner_object.clean_all_data()
                        print("Выполнение программы завершено.")
                        return None
                    if user_response == "2":
                        continue

                # Отмена
                if user_response == "2":
                    break

                else:
                    print("Ошибка: Неизвестный ответ. Выберите 1 или 2.")
                    continue

            # Завершение выполнения программы
            if user_response == "6":
                print("Выполнение программы завершено.")
                return None
            else:
                print("Ошибка: Неизвестный ответ. Выберите 1, 2, 3, 4, 5 или 6")
                continue
