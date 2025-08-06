import os


class EnvFileChecker:
    """
    Вспомогательный класс, содержащий методы проверки необходимых файлов
    """

    def check_dotenv_exists(self) -> bool:
        """
        Метод, проверяющий что файл .env существует
        :return: True / False
        """

        # определение пути до файла .env
        current_dir = os.path.dirname(os.path.abspath(__file__))
        env_file_path = os.path.join(current_dir, "..", ".env")

        # проверка что файл .env создан
        if not os.path.exists(env_file_path):
            return False
        else:
            return True

    def check_dotenv_contents_exist(self) -> bool:
        """
        Метод, проверяющий, что содержимое файла .env существует
        :return: True / False
        """

        # проверка что файл .env существует
        if not self.check_dotenv_exists():
            raise FileNotFoundError("Файл .env отсутствует.")

        if os.getenv('DB_USER') and os.getenv('DB_PASSWORD'):
            return True
        else:
            return False

    def __call__(self):
        if self.check_dotenv_exists() is True and self.check_dotenv_contents_exist() is True:
            return True
        else:
            return False
