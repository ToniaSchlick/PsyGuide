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
$PY manage.py loaddata fixtures/user.json
$PY manage.py loaddata fixtures/patient.json
$PY manage.py loaddata fixtures/questionnaire.json
$PY manage.py loaddata fixtures/flowchart.json
