#!/bin/sh


# Aliases for common commands that take forever to type To enable these
# shortcuts, enter the command `source .command-aliases.sh` at the project
# root.


# Bring up the docker containers for this project (in dev mode)
alias devup="docker-compose -f docker-compose-dev.yml up -d --build"

# Bring down the docker containers
alias devdown="docker-compose -f docker-compose-dev.yml down -v"

# Run all the tests for the flask backend
alias testflask="docker-compose -f docker-compose-dev.yml run --rm flask \
  python manage.py test"

# Run a narrow subset of the flask backend tests.  Define which test
# files to run by modifying the /services/flask/manage.py file
alias testflaskn="docker-compose -f docker-compose-dev.yml run --rm flask \
  python manage.py test_narrow"

# Run the flake8 linter against the flask code
alias lintflask="docker-compose -f docker-compose-dev.yml run --rm flask \
  flake8 project"

# Access the database via the postgresql command line tool
alias psqlcli="docker exec -ti --rm flask-db psql -U postgres -W"

# Recreate the postgresql database
alias recreateDB="docker-compose -f docker-compose-dev.yml run --rm flask \
  python manage.py recreate_db"

flaskCli() {
  # Perform one of the flask cli commands defined in `services/flask/manage.py`
  # When using this function, provide one argument -> the cli command you want
  # to run.
  docker-compose -f docker-compose-dev.yml run --rm flask python manage.py $1
}
