#!/bin/bash

###
# Utility file to perform all setup and load default data easier
###

if [ -x "$(command -v python3)" ]; then
  PY=python3
else
  PY=python
fi

$PY manage.py makemigrations
$PY manage.py migrate
$PY manage.py loaddata user.json
$PY manage.py loaddata base.json
