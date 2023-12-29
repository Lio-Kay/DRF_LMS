# Бэкенд на DRF для LMS веб-приложения

## Описание
REST API на основе DRF для Learning Management System.
Пользователь имеет доступ к разделам, материалам, и тестам.
Регистрация пользователя с кастомными полями на основе 
dj-rest-auth + django-allauth.
Авторизация на основе JWT токенов+возможность дополнительной авторизации 
через dj_rest_auth, верификация почты отправкой письма,
валидация данных на уровне сериализаторов, моделей, и БД.
Проект покрыт unit тестами и имеет OpenAPI документацию. Настроены CORS.

## Инициализация проекта
**Для работы проекта требуется PostgreSQL**
  ```sh
  git clone https://github.com/Lio-Kay/DRF_LMS
  cd DRF_LMS/
  python3 -m venv DRF_LMS
  source DRF_LMS/bin/activate
  pip install -r requirements.txt
  ```
Создайте файл .env рядом с .env.sample и заполните его

Создайте БД Postgres

Запустите через консоль:
  ```sh
  cd lms/
  python manage.py migrate
  python manage.py runserver
  ```
Для наполнения БД данными, используйте кастомные команды, указанные ниже

Документация доступна по адресу:
```
http://127.0.0.1:8000/api/v1/schema/redoc/
```

## Кастомные команды
  ```sh
  python manage.py c_susr
  ```
Создает суперпользователя с параметрами Email: admin@admin.com,
Phone: +1234567890, Password: admin
  ```sh
  python manage.py c_usr
  ```
Удаляет всех пользователей, кроме персонала, и заполняет БД 
новыми пользователями
  ```sh
  python manage.py c_edudata
  ```
Удаляет все данные из education, и заполняет БД новыми данными
## ER-диаграмма моделей

## Описание структуры проекта
* lms
  - accounts - Приложение для работы с пользователями
  - education - Приложение для работы с материалами и тестами к ним
  - lms - Настройки проекта
  - .env.sample - Образец для создания env файла
  - manage.py
* .gitignore
* README.md
* requirements.txt

## Технологии в проекте
Библиотеки:
* Django+DRF
  - dj-rest-auth
  - django-allauth
  - django-cors-headers
  - django-filter
  - django-money
  - django-phonenumber-field
  - djangorestframework-camel-case
  - djangorestframework-simplejwt
  - drf-spectacular
* Faker
* flake8
* Pillow
* psycopg2-binary
* python-dotenv

Другие особенности:
* Покрытие тестами более 92%
* Полное соответствие pep8
* Детальная настройка административной части
