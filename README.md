# Snapp Food

Snapp Food Galaxy

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Black code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

License: MIT

## Getting Started

To start the project, follow these steps:

1. Start the Docker containers:

    ```bash
    sudo docker compose up
    ```

2. Go to the app shell and create a superuser to access the admin panel:

    ```bash
   sudo docker exec -it snapp-app /bin/sh
    python manage.py createsuperuser
    ```

3. Access the admin panel in your web browser at:

    [http://localhost:8000/admin/](http://localhost:8000/admin/)

4. In the admin panel, create some agents, vendors and orders as needed.

## API Endpoints

### Order Delay Report

To create an Order Delay Report, you can use cURL. Replace the number with the order ID:

```bash
curl --location 'http://localhost:8000/api/delay-report/3'
```

### Assign Order to Agent

To assign a delayed order to an agent, you can use cURL.

```bash
curl --location --request POST 'http://localhost:8000/api/assign-order/'
```

### Stores Delay Report

To retrieve Stores Delay Reports, you can use cURL:

```bash
curl --location 'http://localhost:8000/api/receive-delay-reports/'
```
