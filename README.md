# API NoteSnob

## Описание

Проект NoteSnob представляет собой базу отзывов о фильмах, книгах и музыке.

Пользователи могут писать собственную рецензию и ставить оценку произведению по 10-балльной шкале.
Из оценок обзоров формируется средний рейтинг произведения. 
Другие пользователи могут оставлять свои комментарии на рецензии.

## Технические особенности

* При регистрации пользователь оправляет свои данные (username, email), после чего получает на почту
код. Для получения JWT токена аутентификации необходимо отправить username и полученный код с почты.
* Для аутентификации используется **_только Access токен_**. Если необходимо получить токен снова, 
то для этого отправляется новый код на почту.


## Использованные технологии

* [Django 4.2](https://docs.djangoproject.com/en/4.2/)
* [Django REST framework 3.14](https://www.django-rest-framework.org)


## Запуск через Docker

**Клонируйте данный проект:**

```bash
git clone git@github.com:HETPAHHEP/api_notesnob.git
```

**Создайте _dotenv-файл_ и занесите необходимые переменные:**

1) Создание секретного ключа JWT

    ```bash
    openssl rand -hex 32
    ```

2) Создание секретного ключа Django

    ```bash
    ./manage.py shell -c "from django.core.management import utils; 
    print('django-insecure-' + utils.get_random_secret_key())"
    ```

3) Занесите переменные для проекта и своей базы данных _PostgreSQL_

    ```dotenv
    EMAIL=your_sending_email
    JWT_SECRET_KEY=your_jwt_secret_key
    DJANGO_SECRET_KEY=your_django_secret_key
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=password_here
    DB_HOST=db
    DB_PORT=5432
    ```

**Разверните проект с помощью _Docker-compose_:**

```bash
docker-compose up
```


## Данные для тестирования

Для удобной проверки доступны данные в CSV. Чтобы их импортировать в вашу базу данных,
используйте команду в контейнере _web_:

```bash
./manage.py start_import
```

## Документация

Более подробные особенности работы проекта и доступные эндпоинты есть в документации:

**[127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc/)**

P.S. Посмотреть можно на сервере для разработки или подключив nginx для статики (сейчас отсутствует)