#!/usr/bin/env python3

# This script will create the docker-compose-dev.yml and
# docker-compose-prod.yml files.  The docker-compose files are created with
# this script in order to avoid sharing sensitive info in a public repository.

import sys
from string import Template

# The first argument will be used as the postgres password.  If no arguments
# are provided, the postgres password will default to `postgres`
args = sys.argv[1:]
if len(args) > 0:
    postgres_password = args[0]
else:
    postgres_password = 'postgres'

# Define the substitutions that will be made in each file
subs={ 'postgres_password': postgres_password }

# open the template files
dev_template_file = open( 'template-docker-compose-dev.txt' )
prod_template_file = open( 'template-docker-compose-prod.txt' )

# read the template files with Template
dev_template_text = Template( dev_template_file.read() )
prod_template_text = Template( prod_template_file.read() )

# create the text for the docker-compose yml files
dev_text = dev_template_text.substitute(subs)
prod_text = prod_template_text.substitute(subs)

# create the docker-compose-dev.yml file
with open('docker-compose-dev.yml', 'w') as dev_file:
    dev_file.write(dev_text)

# create the docker-compose-prod.yml file
with open('docker-compose-prod.yml', 'w') as prod_file:
    prod_file.write(prod_text)
