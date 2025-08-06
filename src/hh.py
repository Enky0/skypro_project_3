from abc import ABC, abstractmethod

import requests


class BaseAPI(ABC):
    @abstractmethod
    def __init__(self):
        pass

    def __get_vacancies(self):
        pass

    def get_data(self, keyword: str, vacancies_per_page: int = 40):
        pass

    def set_params(self, keyword: str, vacancies_per_page: int = 40):
        pass

    def __call__(self, *args, **kwargs):
        pass


class HH(BaseAPI):
    """
    Класс для работы с API HeadHunter
    """

    def __init__(self):
        """
        Инициализирует API hh.ru
        """
        self.__url = 'https://api.hh.ru/vacancies'
        self.__headers = {'User-Agent': 'HH-User-Agent'}
        self.__params = {'text': '', 'page': 0, 'per_page': 40}
        self.__vacancies = []

    def __get_vacancies(self):
        """
        Метод подключения к API hh.ru
        """
        while self.__params.get('page') != 20:
            response = requests.get(self.__url, headers=self.__headers, params=self.__params)

            response.raise_for_status()  # вызывает requests.exceptions.HTTPError , если статус-код не 200

            vacancies = response.json()['items']

            if not vacancies:
                break

            self.__vacancies.extend(vacancies)
            self.__params['page'] += 1

    def get_data(self, keyword: str, vacancies_per_page: int = 40):
        """
        Метод получения данных с результата поиска вакансий с hh.ru.
        :param keyword: ключевое слово для поиска вакансий, тип str
        :param vacancies_per_page: число вакансий на страницу, тип int
        :return: возвращает список словарей, которые содержат данные о полученных вакансиях
        """
        self.set_params(keyword, vacancies_per_page)
        self.__get_vacancies()
        return self.__vacancies

    def set_params(self, keyword: str, vacancies_per_page: int = 40):
        """
        Метод для работы с методом подключения к API hh.ru, задающий параметры поиска вакансий: ключевое слово и
        количество вакансий на страницу.
        :param keyword: ключевое слово для поиска вакансий, тип str
        :param vacancies_per_page: число вакансий на страницу, тип int
        """
        if not isinstance(keyword, str):
            raise TypeError("Ключевое слово должно быть строкой")
        if not keyword.strip():
            raise ValueError("Строка должна быть не пустая")
        if not isinstance(vacancies_per_page, int):
            raise TypeError("Количество вакансий на страницу должно быть целым числом")
        if not 1 <= vacancies_per_page <= 200:
            raise ValueError("Количество вакансий на страницу должно быть от 1 до 200")

        self.__params['text'] = keyword
        self.__params['per_page'] = vacancies_per_page

    def __call__(self, keyword: str, vacancies_per_page: int = 40) -> list[dict]:
        """
        Вызывает методы для работы с API hh.ru, и выводит полученный результат.
        :param keyword: ключевое слово для поиска вакансий, тип str
        :param vacancies_per_page: число вакансий на страницу, тип int
        :return: возвращает список словарей, которые содержат данные о полученных вакансиях
        """

        result = self.get_data(keyword, vacancies_per_page)
        return result
