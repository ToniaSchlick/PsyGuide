# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.test.client import Client
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from patient.views import *
from patient.forms import PatientForm
from patient.models import Patient
import unittest

#Make sure code runs through
class TestViewFunctions(unittest.TestCase):
    # Set up a logged in user
    def __init__(self):
        self.factory = RequestFactory()
        try:
            self.user = User.objects.create_user(username='jacob', password='top_secret')
        except:
            self.user = Client()
            self.user.login(username='jacob', password='top_secret')


    def test_view_all(self):
        request = self.factory.get('view_all')
        request.user = self.user
        response = index(request)
        assert (response.status_code == 200)


    def test_view(self):
        request = self.factory.get('view')
        request.user = self.user
        response = index(request)
        assert (response.status_code == 200)


    def test_delete_no_auth(self):
        request = self.factory.get('delete')
        request.user = AnonymousUser()
        response = index(request)
        assert (response.status_code == 200)


    def test_delete(self):
        request = self.factory.get('delete')
        request.user = self.user
        response = index(request)
        assert (response.status_code == 200)

    # This essentially tests whether the patient form can be valid. It does not test the backend of saving it.
    def test_add(self):
        #  https://docs.djangoproject.com/en/2.1/topics/testing/tools/#django.test.Client.post
        request = self.factory.get('add')
        request.user = self.user
        response = index(request)
        assert (response.status_code == 200)

        c = Client()
        #c.post('/login/', {'name': 'fred', 'password': 'secret'})

        patient = Patient.objects.create(first_name = "success", last_name = "test", birthday =  "1966-1-02",
                                         diagnosis = "none", current_script = "vitamins", current_dose = "3")
        data = {'first_name': patient.first_name, 'last_name': patient.last_name, 'birthday' : patient.birthday,
                'diagnosis' : patient.diagnosis, 'current_script' : patient.current_script,
                'current_dose' : patient.current_dose}

        pform = PatientForm(data)
        c.post(data)

        assert (response.status_code == 200)



    def test_add_invalid(self):
        patient = Patient.objects.create(first_name="fail", last_name="")
        data = {'first_name': patient.first_name, 'last_name': patient.last_name, }
        pform = PatientForm(data)
        assert not (pform.is_valid())


    def test_edit(self):
        patient = Patient.objects.create(first_name="Manfred", last_name="test", birthday="2000/1/1",
                                         diagnosis="Dp", current_script="vitamins", current_dose="3")
        data = {'first_name': patient.first_name, 'last_name': patient.last_name, 'birthday': patient.birthday,
                'diagnosis': patient.diagnosis, 'current_script': patient.current_script,
                'current_dose': patient.current_dose}
        pform = PatientForm(data)
        assert (pform.is_valid())


class OtherPatientFunctions(unittest.TestCase):
    #This checks to make sure this form is valid
    def test_patient_form(self):
        patient = Patient.objects.create(first_name = "success", last_name = "test", birthday =  "1966-1-02",
                                         diagnosis = "none", current_script = "vitamins", current_dose = "3")
        data = {'first_name': patient.first_name, 'last_name': patient.last_name, 'birthday' : patient.birthday,
                'diagnosis' : patient.diagnosis, 'current_script' : patient.current_script,
                'current_dose' : patient.current_dose}
        pform = PatientForm(data)
        assert (pform.is_valid())


def main():
    myTest = TestViewFunctions()
    myTest.test_view_all()
    myTest.test_view()
    myTest.test_delete_no_auth()
    myTest.test_delete()
    myTest.test_add()
    myTest.test_add_invalid()
    #myTest.test_edit()
    myTest = OtherPatientFunctions()
    #myTest.test_patient_form()



main()
