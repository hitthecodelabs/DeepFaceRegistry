# PROJECT CONFIGURATION
## TIMEZONES
https://en.wikipedia.org/wiki/List_of_tz_database_time_zones


## DIRECTORY PERMISSION
sudo chown -R <username> <directory_name>

## VIRTUAL ENVIRONMENTS

### ACTIVATE POETRY'S SHELL
poetry shell

### EXIT SHELL
exit

## START DOCKER
docker-compose -f camera-track.yml up --build

## CHECK CONTAINER DETAILS
docker inspect <container_id>

## START DOCKER IMAGE PYTHON
docker exec -it <container_id> /bin/bash

## ACCESS PROJECT IN CONTAINER
cd /camera-track

## INSTALL DEPENDENCIES - EACH DEPENDECY INSTALLATION
poetry install

## START PROJECT
poetry run python manage.py runserver

## CREATE MODELS MIGRATIONS - EACH PROJECT MODEL MODIFICATION
poetry run python manage.py makemigrations

## EXECUTE MODELS MIGRATIONS - EACH PROJECT MODEL MODIFICATION
poetry run python manage.py migrate

## CREATE A SUPER USER
poetry run python manage.py createsuperuser

## ACCESS DATABASE
mysql -u <your_user> -h 127.0.0.1 -p<your_password>

## HOW TO EXTRACT BACKUP
docker exec <NAME OR ID> mysqldump -u <USER_NAME> -p<THE_PASSWORD> <YOUR_DB> > prueba_backup.sql

## HOW TO EXTRACT STORE PROCEDURES
docker exec <your_container_id> mysqldump -u <your_user> -p<your_pass> --routines <your_database> > prueba_backup.sql


# PROBLEM SOLVING

## multiple serializers within a single modelviewset
https://stackoverflow.com/questions/22616973/django-rest-framework-use-different-serializers-in-the-same-modelviewset

## methods parameters to accept queryparams or headers
https://stackoverflow.com/questions/23944657/typeerror-method-takes-1-positional-argument-but-2-were-given-but-i-only-pa

## django trailing slash configuration
https://stackoverflow.com/questions/66526285/how-to-solve-django-post-url-error-of-append-slash
https://docs.djangoproject.com/en/dev/ref/settings/#append-slash

## email html template
https://stackoverflow.com/questions/3005080/how-to-send-html-email-with-django-with-dynamic-content-in-it

## django user methods
https://docs.djangoproject.com/en/4.1/ref/contrib/auth/