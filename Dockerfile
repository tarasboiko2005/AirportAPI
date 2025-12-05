# Використовуємо офіційний Python образ
FROM python:3.13-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо requirements
COPY requirements.txt /app/

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код
COPY . /app/

# Відкриваємо порт
EXPOSE 8000

# Запускаємо сервер
CMD ["python", "aviation/manage.py", "runserver", "0.0.0.0:8000"]