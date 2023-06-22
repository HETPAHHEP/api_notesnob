# API NoteSnob ![NoteSnob Workflow](https://github.com/HETPAHHEP/api_notesnob/actions/workflows/notesnob_workflow.yml/badge.svg)

### Описание

Проект NoteSnob представляет собой базу отзывов о фильмах, книгах и музыке.

Пользователи могут писать собственную рецензию и ставить оценку произведению по 10-балльной шкале.
Из оценок обзоров формируется средний рейтинг произведения. 
Другие пользователи могут оставлять свои комментарии на рецензии.

### 🔍 Технические особенности

* При регистрации пользователь оправляет свои данные (username, email), после чего получает на почту
код. 
* Для получения JWT токена аутентификации необходимо отправить username и полученный код с почты.
* Для аутентификации используется **_только Access токен_**. Если необходимо получить токен снова, 
то для этого отправляется новый код на почту.


### 👨‍💻 Использованные технологии

[![Python][Python-badge]][Python-url]
[![Django REST][DRF-badge]][DRF-url]
[![PostgreSQL][Postgres-badge]][Postgres-url]
[![Nginx][Nginx-badge]][Nginx-url]
[![Docker][Docker-badge]][Docker-url]
[![Yandex-Cloud][Yandex-Cloud-badge]][Yandex-Cloud-url]
[![Github-Actions][Github-Actions-badge]][Github-Actions-url]

## ⚙ Начало Работы

Чтобы запустить копию проекта, следуйте инструкциям ниже.


### 🚀 Запуск на сервере

1. **Обновите пакеты**
   
   ```bash
   sudo apt-get update
   sudo apt-get upgrade
   ```

2. **Установите docker compose**
   
   ```bash
   sudo apt-get install docker.io
   sudo apt-get install docker-compose
   ```

3. **Перенесите необходимые файлы**
   
   ```bash
   scp docker-compose.yml <username>@<host>:/home/<username>/
   scp nginx.conf <username>@<host>:/home/<username>/
   scp -r docs/ <username>@<host>:/home/<username>/docs/
   ```

4. **Создайте *dotenv-файл***

   ```bash
   touch .env
   ```

   ```dotenv
   EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
   EMAIL_HOST=your.email.host
   EMAIL_PORT=555
   EMAIL=your@email.com
   EMAIL_PASSWORD=your-sending-email-password
   DJANGO_SECRET_KEY=your-django-secret
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=postgres
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=password_here
   DB_HOST=host_here
   DB_PORT=5432
   ALLOWED_HOSTS=localhost;127.0.0.1;backend;yourhost
   ```
   ###### *Создание секретного ключа JWT*

    ```bash
    openssl rand -hex 32
    ```
   
   ###### *Секретный ключ Django можно сгенерировать [тут](https://djecrety.ir/)*

5. **Добавьте адрес в конфиг nginx**

   ```nginx
   server {
    listen 80;
    server_tokens off;
    server_name yourhost;
   ```

6. **Запустите контейнеры**

   ```bash
   sudo docker-compose up
   ```  

7. **Завершите настройку Django**

   _Чтобы использовать необходимые команды для проекта Django, необходимо выполнять их 
   в нужном контейнере:_
   
   ```bash
   docker exec -it admin_web_1 bash  # имя для примера
   ```

   _Вы можете самостоятельно или с помощью **_entrypoint.sh_** сделать миграции для базы данных
   и собрать статику проекта:_


   - Запустив скрипт
      ```bash
      cat infra/entrypoint.sh | sudo docker exec -i \
      admin_web_1 sh -c 'cat > entry.sh && chmod +x entry.sh && ./entry.sh'
      ```
   - Самостоятельно в контейнере _web_
      ```bash
      python manage.py migrate --no-input
      ```
   
      ```bash
      python manage.py collectstatic --no-input --clear
      ```


---

### 💪 Создание суперпользователя

Чтобы управлять данными приложения и осуществлять наблюдения за работой проекта, необходимо
создать суперпользователя. Он будет иметь права роли администратора и доступ к панели Django. 

```bash
python manage.py createsuperuser
```

### 📇 Данные для тестирования

Для удобной проверки доступны данные в CSV. Чтобы их импортировать в базу данных,
используйте данную команду в контейнере _web_:

```bash
python manage.py start_import
```

### 🗑 Отчистка данных

Если необходимо на сервере полностью отчистить запущенные контейнеры и их зависимости,
то для этого можно воспользоваться следующей командой:

```bash
sudo docker-compose down -v --rmi
```

### 📖 API (Docs: [OpenAPI](notesnob_api/static/redoc_notesnob.yaml))

Документация доступна по ссылке: http://localhost/redoc

   ###### **Локальный эндпоинт*


---

<h5 align="center">
Автор проекта: <a href="https://github.com/HETPAHHEP">HETPAHHEP</a>
</h5>

<!-- MARKDOWN BADGES & URLs -->
[Python-badge]: https://img.shields.io/badge/Python-4db8ff?style=for-the-badge&logo=python&logoColor=%23ffeb3b

[Python-url]: https://www.python.org/

[Gunicorn-badge]: https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white

[Gunicorn-url]: https://gunicorn.org/

[Postgres-badge]: https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white

[Postgres-url]: https://www.postgresql.org/

[Docker-badge]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white

[Docker-url]: https://www.docker.com/

[Nginx-badge]: https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white

[Nginx-url]: https://nginx.org

[DRF-badge]: https://img.shields.io/badge/Django_REST-f44336?style=for-the-badge&logo=django

[DRF-url]: https://www.django-rest-framework.org

[Yandex-Cloud-badge]: https://img.shields.io/badge/Yandex_Cloud-white?style=for-the-badge

[Yandex-Cloud-url]: https://cloud.yandex.ru

[Github-Actions-badge]: https://img.shields.io/badge/Github_Actions-%239c27b0?style=for-the-badge&logo=github%20actions&logoColor=white

[Github-Actions-url]: https://github.com/features/actions