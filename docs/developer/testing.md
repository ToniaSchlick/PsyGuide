# Unit Tests

PsyGuide uses unit testing done through Django's standard hierarchy.  A `tests.py` file can be found in each app's directory, containing tests related to that app's views and models.

## Testing Automation

PsyGuide uses Travis-CI to run these unit tests on each commit.  Testing a Django app this way is somewhat complex, as there's some config overhead in `.travis.yml`.  Testing in Django is done from the Django project root, so python must be called from that directory.  Additional setup is needed to get the project in a testable form in the Travis VM, and `makemigrations` and `migrate` must be called before the final `python manage.py test` command can be called to run all of the tests.

## Manual Testing

The unit tests can be executed with `manage.py` just like any other project function.  Simply navigate to the `/PsyGuideSite/` directory and run `python manage.py test`.  Note that if you encounter any errors, you may need to first migrate by running `python manage.py makemigrations` and `python manage.py migrate`.

## Adding Tests

Adding a test is as simple as adding another class to the `tests.py` file in whichever app you'd like to test.  The only restriction is the class must have a `setUp()` method as well as actual test methods that are prefixed with `test_`.  The Django TestRunner will automatically discover these classes and run the `test_*` methods.

**Note that the database used when running tests is distinct from the live database.  As such, no objects will be present other than the ones you create in your tests.**

# Code Coverage

In addition to CI testing, PsyGuide makes use of Coveralls for code coverage viewing.  Travis handles sending the coverage report data directly to Coveralls, configured in `.travis.yml`.  The coverage report badge is shown at the top of the README, and the report can also be seen directly [here](https://coveralls.io/github/friday-the-13th/Front-end).

# Selenium

In addition to unit testing, PsyGuide also uses Selenium to facilitate end-to-end tests.  These can be found in `/tests/PsyGuideSelenium.side`, and it's tests can be run using the Selenium-IDE browser extension.  **These tests are not currently automated**, however they should be run periodically and before releases to ensure user functionality.
