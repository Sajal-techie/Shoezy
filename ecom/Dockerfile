# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /code

# Copy requirements.txt and install dependencies
COPY requirements.txt .

RUN python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
# Copy the rest of the project files
COPY . .

RUN python manage.py collectstatic --noinput

# Expose the default Django port
EXPOSE 8000

# Run the development server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ecom.wsgi:application"]
