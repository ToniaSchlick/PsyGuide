# Project Layout

```text
    Front-end/      # Repo root
        docs/       # Documentation root

        PsyGuideSite/               # Root of Django project
            docs/                   # All Documentation
            fixtures/               # Dummy data for testing
            flowchart/              # Flowchart app
            patient/                # Patient app
            prescriber/             # Prescriber app (home page)
            PsyGuideSite/           # Django project root
            questionnaire/          # Questionnaire app

            setup.sh                # Utility file for running test server
            install_dependencies.sh # Utility file for first time setup
            ...                     # Other django project files

        static/     # Static files for django test server
            css/
            img/
            js/

        tests/      # Project wide tests
```

# App Structure

Each app flowchart, patient, prescriber and questionnaire has the following structure:

```text
    <app_name>/
        migrations/
        templates/
            <app_name>/
                snippets/   # Small reusable components like cards or forms
                
                *.html      # Django template files for rendering in views

        __init__.py     # Empty, python module recognition
        admin.py        # Admin panel specific settings
        apps.py         # Django app name set
        models.py       # Classes related to the app
        tests.py        # Unit tests specific to app
        urls.py         # App urls, usually of the form <hostname>/<app_name>/*
        views.py        # Rendering of templates in functions passed to by a url
```

PsyGuide follows the standard Django project conventions for the most part, and as such more information can be found by looking into Django's official documentation [here](https://docs.djangoproject.com/en/2.2/intro/tutorial01/)
