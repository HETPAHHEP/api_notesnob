# API NoteSnob
pyth
![NoteSnob Workflow](https://github.com/HETPAHHEP/api_notesnob/actions/workflows/notesnob_workflow.yml/badge.svg)

## Описание

Проект NoteSnob представляет собой базу отзывов о фильмах, книгах и музыке.

Пользователи могут писать собственную рецензию и ставить оценку произведению по 10-балльной шкале.
Из оценок обзоров формируется средний рейтинг произведения. 
Другие пользователи могут оставлять свои комментарии на рецензии.

## Технические особенности

* При регистрации пользователь оправляет свои данные (username, email), после чего получает на почту
код. Для получения JWT токена аутентификации необходимо отправить username и полученный код с почты.
* Отправка письма происходит через SMTP сервер Яндекса.
* Для аутентификации используется **_только Access токен_**. Если необходимо получить токен снова, 
то для этого отправляется новый код на почту.


## Использованные технологии

* [Python 3.11](https://www.python.org/downloads/release/python-3110/)
* [Django 4.2](https://docs.djangoproject.com/en/4.2/)
* [Django REST framework 3.14](https://www.django-rest-framework.org)
* [PostgreSQL 15.3](https://www.postgresql.org/docs/15/release-15-3.html)
* [Nginx](https://nginx.org/en/)
* [Docker](https://www.docker.com)


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
    EMAIL_PASSWORD=your_app_password
    JWT_SECRET_KEY=your_jwt_secret_key
    DJANGO_SECRET_KEY=your_django_secret_key
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=password_here
    DB_HOST=db
    DB_PORT=5432
    ```

**Занесите адрес сервера в конфигурационный файл _nginx_:**
   ```bash
   cp -r api_notesnob/infra/. ~  # копирование файлов из проекта
   ```
   
   ```bash
   nano nginx/default.conf  # редактировать настройки
   ```

**Разверните проект с помощью _Docker-compose_:**

Если будет использоваться образ проекта Django c Docker Hub, то можно просто запустить нужную
команду.

```bash
docker-compose up
```

_или_

```bash
sudo docker compose up
```

При необходимости можно собрать и через Dockerfile, но изменив при этом docker-compose.

## Запуск команд

Чтобы использовать необходимые команды для проекта Django, необходимо войти в контейнер:

```bash
docker exec -it api_notesnob-web-1 bash  # пример
```

После чего самостоятельно или с помощью _entrypoint.sh_ сделайте миграции для базы данных
и соберите статику проекта:

1) Запустив скрипт
   ```bash
   cat infra/entrypoint.sh | sudo docker exec -i \
   ilya-web-1 sh -c 'cat > entry.sh && chmod +x entry.sh && ./entry.sh'
   ```
2) Самостоятельно
   ```bash
   python manage.py migrate --no-input
   ```
   
   ```bash
   python manage.py collectstatic --no-input --clear
   ```


---

### Создание суперпользователя

Чтобы управлять данными приложения и осуществлять наблюдения за работой проекта, необходимо
создать суперпользователя. Он будет иметь права роли администратора и доступ к панели Django. 

```bash
python manage.py createsuperuser
```

### Данные для тестирования

Для удобной проверки доступны данные в CSV. Чтобы их импортировать в вашу базу данных,
используйте данную команду в контейнере _web_:

```bash
python manage.py start_import
```

### Отчистка данных

Если необходимо на сервере полностью отчистить запущенные контейнеры и их зависимости,
то для этого можно воспользоваться следующей командой:

```bash
sudo docker compose down -v --rmi
```

## Документация

Более подробные особенности работы проекта и доступные эндпоинты есть в документации:

**[127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc/)** — эндпоинт для локальной разработки
