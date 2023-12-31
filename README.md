# Трекер полезных привычек 

Приложение позволяет пользователю создавать привычки и получать напоминание в мессенджере Telegram о необходимости 
выполнения 

# Установка
### Клонируйте репозиторий на свой локальный компьютер:
`git clone [<URL репозитория>](https://github.com/RObotiaga/DRFCourse)`

### Перейдите в каталог проекта:
`cd DRFCourse`

### Установите зависимости, используя poetry:
`poetry install`
# Запуск
### Запустите сервер 
`python manage.py runserver`
### Запустите celery
```
celery -A CourseDRF worker -l INFO -P eventlet -S django
celery -A CourseDRF beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```
# Настройка
Для работы сервиса необходимо настроить некоторые параметры, такие как база данных и настройки email-отправки. Вам потребуются следующие параметры, которые вы можете установить в файле .env:
```
DEBUG=True

DB_NAME=DjangoCourseDRF
DB_USER=postgres
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=5432

ACCESS_TOKEN_LIFETIME=1500
REFRESH_TOKEN_LIFETIME=15

REDIS_HOST=redis://127.0.0.1:6379

TELEBOT_API=
```
Независимо от способа создания привычки пользователем, для получения напоминаний от бота необходимо написать любое сообщение.
После создания пользователем полезной привычки будет создана периодическая задача, результатом выполнения которой будет 
отправка сообщения в телеграм в заданное пользователем время с заданной периодичностью

# Docker
Создайте файл .env и установите необходимые переменные окружения:
```
DEBUG=True

DB_NAME=
DB_USER=postgres
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432

ACCESS_TOKEN_LIFETIME=1500
REFRESH_TOKEN_LIFETIME=15

EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
REDIS_HOST=redis://127.0.0.1:6379

TELEBOT_API=
```
Запустите проект с помощью Docker Compose:
`docker-compose up -d`