# Use the official Python image as a parent image
FROM python:3.10.12

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY app/requirements/base.txt /app/
COPY app/requirements/production.txt /app/

# Install dependencies
RUN pip install -r production.txt

# Copy the rest of your application's code to the container
COPY app /app/

# Expose the port your application runs on
EXPOSE 8000

# Start your application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
