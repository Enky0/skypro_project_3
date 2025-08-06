class VacancyFilter:
    """
    Вспомогательный класс класса Vacancy.
    Выполняет функцию фильтрации вакансий в нескольких режимах
    """

    def __init__(self, vacancies: list[dict]):
        self.__raw_vacancies = vacancies

    def __validate_data(self):
        """
        Метод для валидации
        :return: Возвращает True, если переданные данные являются списком словарей, False если нет
        """
        if isinstance(self.__raw_vacancies, list):
            if all(isinstance(item, dict) for item in self.__raw_vacancies):
                return True
        else:
            return False

    def __get_not_unique_employers_id(self) -> list:
        """
        Метод для создания списка, который содержит не уникальные id всех работодателей.
        Необходим для методоа __get_top_employers_id()
        :return: Список, содержащий id работодателей
        """
        # список всех id работодателей
        employers_id_list = [employer['employer']['id'] for employer in self.__raw_vacancies]

        return employers_id_list

    def __get_unique_employers_id(self) -> list:
        """
        Метод получает список уникальных id работодателей. Необходим для методоа __get_top_employers_id()
        :return: Список, содержащий id работодателей.
        """
        not_unique_id_list = self.__get_not_unique_employers_id()
        unique_id_list = []

        for employer_id in not_unique_id_list:
            if employer_id not in unique_id_list:
                unique_id_list.append(employer_id)

        return unique_id_list

    def __get_top_employers_id(self):
        """
        Метод для записи работодателей в список. Список составлен от работодателя с наибольшим количеством вакансий,
        до работодателя с наименьшим количеством вакансий.
        :return: Список, содержащий id работодателей.
        """
        # подсчет количества id в списке
        employer_counts = {}
        for employer_id in self.__get_not_unique_employers_id():
            employer_counts[employer_id] = employer_counts.get(employer_id, 0) + 1

        # Сортируем список id
        sorted_employers_id_list = sorted(employer_counts, key=employer_counts.get, reverse=True)[:10]

        return sorted_employers_id_list

    def get_vacancies_by_top_employers(self):
        """
        Метод создает список, и записывает в него только словари, в которых ключ['employer']['id'] совпадает со
        списком топа-10 работодателей
        :return: список вакансий только топа-10 работодателей
        """
        top_employers = []
        employers_id = self.__get_top_employers_id()
        for vacancy in self.__raw_vacancies:
            for employer_id in employers_id:
                if vacancy['employer']['id'] == employer_id:
                    top_employers.append(vacancy)

        return top_employers
