# How to run it

To start the project, use this command:

```shell
docker-compose -f deploy/docker-compose.yml --project-directory . up --build
```

# Migrations

To migrate your database, run this commands:

```shell
poetry run python manage.py makemigrations --settings=config.settings_dev; poetry run python manage.py migrate --settings=config.settings_dev
```

# API Documentation

The projects use Swagger to document the API. After running the project, got to 
`http://0.0.0.0:8000/swagger/` or `http://0.0.0.0:8000/redoc/` to see all endpoints.
