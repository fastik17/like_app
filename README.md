### API documentation

API documentation can be found following these links

Redoc documentation

<api_url>/docs

# CLEARBIT AND HUNTER.IO 

In this project contains the following services such a:
- [Hunter](https://hunter.io)
- [Clearbit](https://clearbit.com/)
They have free pricing plans, so please register and use your own token for testing app


# Docker setup

Development highly bound to docker, so there is docker-compose-dev.yml for development and
run python manage.py runserver and ... by your PyCharm IDE.

NOTE you need to pass environment variable in your PyCharm Run configuration.

If you want to keep virtual environment in the project's level set PIPENV_VENV_IN_PROJECT=1
to your host machine env vars before creating pipenv environment.

# Local Setup (Alternative to Docker)

Recommended Installation

1. Postgresql
2. Python 3.8

Installation

1. Install pipenv 
2. Clone this repo and cd like_app
3. Run pip install --user --upgrade pipenv to get the latest pipenv version.
4. Run pipenv --python 3.8
5. Run pipenv install
6. Run cp .env.example .env
7. Update .env file DATABASE_URL with your database_name, database_user, database_password, if you use postgresql. Can alternatively set it to sqlite:////tmp/my-tmp-sqlite.db, if you want to use sqlite for local development.

Getting Started

1. Run pipenv shell
2. Run python manage.py makemigrations
3. Run python manage.py migrate
4. Run python manage.py runserver