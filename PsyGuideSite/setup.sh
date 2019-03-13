#!/bin/bash

###
# Utility file to perform all setup and load default data easier
###

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata base.json
