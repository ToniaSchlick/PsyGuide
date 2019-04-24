from django.test import TestCase
from questionnaire.views import *


class TestViewFunctions(TestCase):
    # Set up a logged in user for the tests
    def __init__(self):
        self.factory = RequestFactory()
        try:
            self.user = User.objects.create_user(username='jacob', password='top_secret')
        except:
            self.user = Client()
            self.user.login(username='jacob', password='top_secret')


    def test_function(self, name):
        request = self.factory.get(str(name))
        request.user = self.user
        response = eval(name)(request)
        assert (response.status_code == 200)


    def test_administer(self):
        self.test_function('administer')


    def test_create(self):
        self.test_function('create')


    def test_view_all(self):
        request = self.factory.get('view_all')
        request.user = self.user
        response = viewAll(request)
        assert (response.status_code == 200)

class TestQuestionnaireModel(TestCase):
    def __init__(self):

        pass

    def test_add_question(self):
        pass


def main():
    myTest = TestViewFunctions()
    myTest.test_view_all()
    myTest.test_create()
    myTest.test_administer()


main()
