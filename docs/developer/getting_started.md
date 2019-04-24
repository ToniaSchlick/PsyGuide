# Prerequisites

PsyGuide is built with Django, and as such, Python3 and Django are required.  Additional packages such as django-crispy-forms and simpleeval are used for various specific functions across the project.

## Installation

A utility file ```install_dependencies.sh``` is provided in the ```PgyGuideSite/``` directory, which when run with some form of Bash will automatically install all of the packages that PsyGuide requires.


### Manual installation

If for some reason you'd rather not run the sh file, ensure you have pip installed then run the following commands:

```text
    pip install django
    pip install django-crispy-forms
    pip install simpleeval
```

You should now have everything you need to get the project running.

# Running The Test Server


Ensure you're in the Django project root, which is in ```<repo_root>/PsyGuideSite/```.  Be sure to run ```./setup.sh``` to get a clean slate first before starting the server.  Then starting the server is as simple as running the command ```python manage.py runserver```. The test server should then be live at ```localhost:8000``` on your machine.

## Default Login

The default login provided for debugging purposes is:

    Username: dev
    Password: 423Team13
