# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app/aviation/

# Copy requirements
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy all source code
COPY . /app/

# Expose port
EXPOSE 8000

# Run server
# CMD ["gunicorn", "aviation.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]

# Run server
#CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "aviation.asgi:application"]

CMD ["uvicorn", "aviation.asgi:application", "--host", "0.0.0.0", "--port", "8000"]