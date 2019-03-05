

# from file import function, for example: from prescriber.admin import adminFunction
from prescriber.exampleTest import aFunction


# Note: The name of this file must start with test_, as well as the test functions. This is only because of pytest.
## A dummy template for how to format tests
# def test_aFunction():
#     assert(someFunction((myInput) == functionOutput))


def test_example():
    assert(travisTest(10) == 10)
