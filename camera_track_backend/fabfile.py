from fabric import task


@task
def migrations(c):
    c.run("poetry run python manage.py makemigrations")


@task
def migrate(c):
    c.run("poetry run python manage.py migrate")


@task
def serve(c):
    # c.run("poetry run python manage.py runserver 0.0.0.0:8000")
    c.run("poetry run python manage.py runserver localhost:8000")


@task
def user(c):
    c.run("poetry run python manage.py createsuperuser")
