# Use official Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code
COPY . /app/

# Expose port
EXPOSE 8000

# Run server
CMD ["python", "aviation/manage.py", "runserver", "0.0.0.0:8000"]