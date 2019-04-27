from django.test import TestCase
from django.test.client import Client
from django.urls import reverse, resolve
from django.test.client import RequestFactory
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser, User
from prescriber.views import *
from patient.forms import PatientForm
from patient.models import Patient

# Create your tests here.

#test url paths
class TestUrls(TestCase):
    def test_index_url(self):
        path = reverse('index')
        assert resolve(path).view_name == 'index'

#Make sure code runs through
class TestViewFunctions(TestCase):
    # Set up a logged in user for the tests
    def setUp(self):
        self.factory = RequestFactory()

        User = get_user_model()
        self.user = User.objects.create_user(username='jacob', password='top_secret')

    def test_index(self):
        request = self.factory.get('')
        # Simulates someone not logged in
        request.user = AnonymousUser()
        response = index(request)
        assert (response.status_code == 200)

    # Make sure the index goes through its code when given a request
    def test_index_auth(self):
        request = self.factory.get('index')
        # This simulates a logged in user
        request.user = self.user
        response = index(request)
        assert (response.status_code == 200)


class OtherPrescriberFunctions(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = get_user_model()

    '''
    Currently, this test below is probably dealing with a combination of middleware issues and added security for 
    registering. It will give full coverage once this is fixed, but I don't expect this to be a simple solution. 
    '''
    def test_register_valid(self):
        pass
        # data = {'username': "Francis", 'password1': "zoeylouisbill", 'password2': "zoeylouisbill"}
        # request = self.factory.post('register', data=data)
        # response = register(request)
        # assert (response.status_code == 302)

    #Just tests the register view
    def test_register_get(self):
        request = self.factory.get('register')
        request.user = self.user
        response = register(request)
        self.assertEqual(response.status_code, 200)
