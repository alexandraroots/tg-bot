# Используем официальный образ Python как базовый
FROM python:3.9-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем только файл requirements.txt вначале, чтобы воспользоваться кэшированием слоев Docker
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем остальные файлы бота в контейнер
COPY . /app

# Запускаем бота при старте контейнера
CMD ["python", "./quiz_bot.py"]
