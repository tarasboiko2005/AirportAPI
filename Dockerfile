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

# Run server (ASGI via Uvicorn)
CMD ["uvicorn", "aviation.asgi:application", "--host", "0.0.0.0", "--port", "8000"]