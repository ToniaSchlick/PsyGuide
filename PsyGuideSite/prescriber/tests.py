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


    def test_register_view(self):
        request = self.factory.get('delete')
        request.user = self.user
        response = register(request)
        assert (response.status_code == 200)


class OtherPrescriberFunctions(TestCase):
    #Test registering a form
    #TODO - alter to fit registration form
    def test_register_valid(self):
        c = Client()
        c.post('/login/', {'name': 'fred', 'passwd': 'secretpiepie'})

        patient = Patient.objects.create(first_name = "success", last_name = "test")
        data = {'first_name': patient.first_name, 'last_name': patient.last_name, 'password' : patient.birthday}
        pform = PatientForm(data)
        assert (pform.is_valid())


    def test_register_invalid(self):
        c = Client()
        c.post('/login/', {'name': 'fred', 'passwd': 'secret'})

        patient = Patient.objects.create(first_name="fail", last_name="")
        data = {'first_name': patient.first_name, 'last_name': patient.last_name, }
        pform = PatientForm(data)
        assert not (pform.is_valid())
