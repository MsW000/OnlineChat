#1. Базовый образ с python
FROM python:3.11-slim

#2. Устанавливаем системные зависимости (для postgresql клиента и других)
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

#3. Устанавливаем рабочую директорию
WORKDIR /app 

#4. Копируем файл зависимостей
COPY requirements.txt .

#5. Устанавливаем python зависимости
RUN pip install --no-cache-dir -r requirements.txt

#6. Копируем весь проект
COPY . .

#7. Открываем порт для FastApi
EXPOSE 8000 

#8. Запускаем приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]