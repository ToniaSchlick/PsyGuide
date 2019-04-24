#!/bin/bash

###
# Utility file to install all required dependencies
###

if [ -x "$(command -v pip3)" ]; then
  PIP=pip3
else
  PIP=pip
fi

$PIP install django
$PIP install django-crispy-forms
$PIP install simpleeval
