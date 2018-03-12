#!/bin/sh

alias testflask="docker-compose -f docker-compose-dev.yml run flask python manage.py test"
alias lintflask="docker-compose -f docker-compose-dev.yml run flask flake8 project"
alias devup="docker-compose -f docker-compose-dev.yml up -d --build"
alias devdown="docker-compose -f docker-compose-dev.yml down -v"
