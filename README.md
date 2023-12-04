# Бэкенд на DRF для LMS веб-приложения

## Описание
REST API на основе DRF для Learning Management System.
Пользователь имеет доступ к разделам, материалам, и тестам.
Авторизация на основе JWT токенов, валидация на уровне сериализаторов и моделей.
Проект покрыт unit тестами и задокументирован.

## Инициализация проекта
**Для работы проекта требуется PostgreSQL**
  ```sh
  git clone https://github.com/Lio-Kay/DRF_LMS
  cd DRF_LMS/
  pip install -r requirements.txt
  ```
Создайте файл .env рядом с .env.sample и заполните его

Создайте БД Postgres

Запустите через консоль:
  ```sh
  cd lms/
  python manage.py migrate
  python manage.py loaddata data.json
  python manage.py runserver
  ```
Документация доступна по адресу:
```
http://127.0.0.1:8000/api/v1/redoc/
```
Для входа в административную часть сайта используйте:
```
Логин:
admin@admin.com

Пароль:
1234
```

## ER-диаграмма моделей

## Описание структуры проекта
* lms
  - education - Приложение для работы с материалами и тестами к ним
  - lms - Настройки проекта
  - users - Приложение для работы с пользователями
  - .env.sample - Образец для создания env файла
  - data.json - Образцы данных для БД
  - manage.py
* .gitignore
* README.md
* requirements.txt

## Технологии в проекте
Библиотеки:
* Django+DRF
  - drf-yasg
  - djangorestframework-simlejwt
  - django-cors-headers
  - django-money
  - django-phonenumber-field
* psycopg2-binary
* python-dotenv

Другие особенности:
* Покрытие тестами более 90%
* Почти полное соответствие pep8
* Настроены CORS
* Документация эндпоинтов на основе OpenAPI
