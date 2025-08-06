from dotenv import load_dotenv

load_dotenv()  # загрузка переменных окружения нужна до импорта UserInteraction, иначе сломается

from src.user_interaction import UserInteraction


def main():
    ui_object = UserInteraction
    ui_object.interaction_with_user()


if __name__ == "__main__":
    main()
