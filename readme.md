Бот, позволяющий осуществлять создание задач, отслеживать их выполнение и уведомлять пользователя о необходимости 
выполнения задачи. Основой бота является библиотека pytelegrambotapi, в качестве СУБД для хранения данных  используется 
Postgresql взаимодействие с базой данных осуществляется на основе Django ORM. Логирование ведётся с помощью библиотеки loguru

python=3.9

Основные используемые библиотеки:
pytelegrambotapi = 4.5.1
django = 4.0.4
psycopg2 = 2.9.3
loguru = 0.6.0

Также для работы необходима установленная СУБД Postgresql. Все необходимые зависимости для проекта описаны в файле requirements.txt
В файле settings.py необходимо прописать имя базы, имя пользователя и пароль. А также токен бота в переменную TOKEN. Путь к файлу: ./todobot/settings.py
Значения хранятся в списке DATABASES

Пример конфига
```python
SECRET_KEY = ""
DEBUG = True

BOT_TOKEN = ""
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': "",
        'USER': "",
        'PASSWORD': ""
    }
}
```


Для развертывания проекта необходимо параллельно запустить два скрипта и сервер на джанго :

1) python manage.py runserver
2) python manage.py telegram_bot // Модуль телеграм бота
3) python manage.py annunciator // Модуль для отправки уведомлений

Также необходимо произвести миграции с базой:

1) python manage.py makemigrations
2) python manage.py migrate

Для запуска бота необходимо отправить ему команду "/start"