# Приложение для поиска вакансий на hh.ru с подключением к БД
## Описание:
Приложение создает базу данных с таблицами для работодателя и для вакансий, выполняет поиск вакансий через API hh.ru, и записывает результаты поиска в базу данных по 10-и работодателям с самым большим количеством активных вакансий.
## Установка
Клонируйте репозиторий:

**SSH:**

```git clone git@github.com:Enky0/skypro_project_3.git```

**HTTPS:**

```git clone https://github.com/Enky0/skypro_project_3.git```

---
Установите PostgreSQL:

Windows: https://www.postgresql.org/download/windows/

macOS: https://www.postgresql.org/download/macosx/

---
Зависимости:

Установите Poetry:
```curl -sSL https://install.python-poetry.org | python3 -```

Установите зависимости:

```poetry install```

# Запуск

Для запуска напишите в терминал:

```python -m src.main```

Далее, следуйте инструкциям программы.