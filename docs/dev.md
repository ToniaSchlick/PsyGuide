# Developer Documentation

## Project layout

```text
    Front-end/      # Repo root
        docs/       # Documentation root

        PsyGuideSite/               # Root of Django project
            docs/                   # All Documentation
            fixtures/               # Dummy data for testing
            flowchart/              # Flowchart app
                templates/          # Django templates for
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

## Patient App

The patient app is used to store and manage patient specific information, like first/last name and date of birth.
