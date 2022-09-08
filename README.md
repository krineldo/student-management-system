# student-management-system

A simple university user system application

## Run project with Django development server

Enter the commands:

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py makemigrations

python manage.py runserver
```

## Run project with Docker

Enter the commands:

```bash
docker-compose up --build
```

## Before running the project Create a .env file
```
DATABASE_NAME=student_management_db
DATABASE_USER=<your postgres user>
DATABASE_PASS=<your postgres password>

# Use the same name from docker-compose.yml
DOCKER_DATABASE_HOST=db
```