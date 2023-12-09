# Используем базовый образ Python
FROM python:3

# Устанавливаем рабочую директорию в контейнере
WORKDIR /code

# Копируем файлы Poetry в контейнер
COPY pyproject.toml .
COPY poetry.lock .

# Устанавливаем Poetry в контейнере
RUN pip install poetry

# Устанавливаем зависимости через Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi


# Копируем код приложения в контейнер
COPY . .
