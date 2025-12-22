# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app/aviation/

# Copy requirements
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN pip install google-genai

# Copy all source code
COPY . /app/

# Expose port
EXPOSE 8000

# Run server
CMD ["gunicorn", "aviation.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]