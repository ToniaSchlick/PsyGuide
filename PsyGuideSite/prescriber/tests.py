# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse, resolve
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from prescriber.views import *
from patient.forms import PatientForm
from patient.models import Patient

import unittest

# Create your tests here.

#test url paths
class TestUrls:

    def test_index_url(self):
        path = reverse('index')
        assert resolve(path).views_name == 'index'

#Make sure code runs through
class TestViewFunctions(unittest.TestCase):

    # https://docs.djangoproject.com/en/2.1/topics/testing/advanced/#the-request-factory
    # Set up a logged in user
    def __init__(self):
        self.factory = RequestFactory()
        # Creates a user for us to simulate, or logs one in for us
        try:
            self.user = User.objects.create_user(username='jacob', password='top_secret')
        except:
            self.user = Client()
            self.user.login(username='jacob', password='top_secret')


    def test_index(self):
        request = self.factory.get('')
        # Simulates someone not logged in
        request.user = AnonymousUser()
        response = index(request)
        #self.assertEqual(response.status_code, 200)
        assert (response.status_code == 200)


    # Make sure the index goes through its code when given a request
    def test_index_auth(self):
        request = self.factory.get('index')
        # This simulates a logged in user
        request.user = self.user
        response = index(request)
        assert (response.status_code == 200)

    #Test registering a form
    def test_register_valid(self):
        patient = Patient.objects.create(first_name = "success", last_name = "test", birthday =  "6/6/2010",
                                         diagnosis = "none", current_script = "vitamins", current_dose = "3")
        data = {'first_name': patient.first_name, 'last_name': patient.last_name, 'birthday' : patient.birthday,
                'diagnosis' : patient.diagnosis, 'current_script' : patient.current_script,
                'current_dose' : patient.current_sdose}
        pform = PatientForm(data)
        assert (pform.is_valid())


    def test_register_invalid(self):
        patient = Patient.objects.create(first_name="fail", last_name="")
        data = {'first_name': patient.first_name, 'last_name': patient.last_name, }
        pform = PatientForm(data)
        assert not (pform.is_valid())


def main():
    myTest = TestViewFunctions()
    myTest.test_index()
    myTest.test_register_invalid()
    myTest.test_register_invalid()
main()