class Vacancy:
    """
    Класс для работы с вакансиями, полученными с json-ответа API hh.ru
    """
    def __init__(self, vacancies: list[dict]):
        self.__raw_vacancies = vacancies
        self.__filtered_vacancies = []

    def __validate_data(self) -> bool:
        """
        Метод для проверки правильности переданных данных
        :return: bool
        """
        if isinstance(self.__raw_vacancies, list):
            if all(isinstance(item, dict) for item in self.__raw_vacancies):
                return True
        else:
            return False

    def __shorten_vacancies(self):
        """
        Метод записывает в список __filtered_vacancies словари с вакансиями без лишних ключ-значений
        """
        if not self.__validate_data():
            raise TypeError("Переданные данные должны быть списком словарей")

        for vacancy_data in self.__raw_vacancies:
            # вариант если зарплата не указана
            if vacancy_data.get("salary") is not None:
                if vacancy_data["salary"].get("from") is None:
                    vacancy_data["salary"]["from"] = 0.0
            else:
                vacancy_data["salary"] = {"from": 0.0}

            dict_data = {
                "vacancy_id": vacancy_data.get("id"),
                "vacancy_name": vacancy_data.get("name"),
                "vacancy_requirements": vacancy_data.get("snippet").get("requirement"),
                "vacancy_salary": vacancy_data.get("salary").get("from"),
                "vacancy_url": vacancy_data.get("alternate_url"),
                "employer_id": vacancy_data.get("employer").get("id"),
                "employer_name": vacancy_data.get("employer").get("name")
            }

            if dict_data['vacancy_requirements'] is None:
                dict_data['vacancy_requirements'] = "Требования не указаны."

            self.__filtered_vacancies.append(dict_data)

    def get_vacancies(self) -> list[dict]:
        """
        Метод возвращает 'укороченный' список вакансий
        :return: Список вакансий в виде списка словарей
        """
        self.__shorten_vacancies()
        return self.__filtered_vacancies
