# Используем официальный образ Python
FROM python:3.12.4

# Устанавливаем рабочую директорию
WORKDIR /code

# Копируем файл зависимостей
COPY ./requirements.txt /code/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade setuptools
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN pip install --no-cache-dir python-multipart

# Копируем весь код приложения
COPY ./ /code

# Создаем директории для статических файлов
RUN mkdir -p /code/static/images /code/static/videos

# Команда для запуска FastAPI сервера
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
