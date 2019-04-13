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
    # Set up a logged in user for the tests
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
        response = viewAll(request)
        assert (response.status_code == 200)


    def test_view(self):
        request = self.factory.get('view')
        #print("View request-",request)
        request.user = self.user
        response = view(request)
        assert (response.status_code == 200)


    def test_delete_no_auth(self):
        request = self.factory.get('delete')
        # print("Hugh's delete request-",request)
        # request += "/?pk=999"
        # print("Hugh's new delete rqt-",request)
        request.user = AnonymousUser()
        response = delete(request)

        # Makes and then deletes a patient. Though it doesn't yet go through the direct code, it does use the same code.
        patient = Patient.objects.create(first_name="Nibbens", last_name="Deathstar", birthday="1966-1-02",
                                         diagnosis = "other", current_script = "vitamins", current_dose = "3", pk = 999)
        patient.delete()

        assert (response.status_code == 200)


    def test_delete(self):
        request = self.factory.get('delete')
        request.user = self.user
        response = delete(request)
        assert (response.status_code == 200)

    # This essentially tests whether the patient form can be valid. It does not test the backend of saving it.
    def test_add(self):
        #  https://docs.djangoproject.com/en/2.1/topics/testing/tools/#django.test.Client.post
        request = self.factory.get('add')
        request.user = self.user
        response = add(request)
        assert (response.status_code == 200)

    # This is meant to test whether a valid form goes through properly
    # https://test-driven-django-development.readthedocs.io/en/latest/05-forms.html   to test forms
    def test_add_valid(self):
        request = self.factory.get('add')
        request.user = self.user

        patient = Patient(first_name = "Aibbens", last_name = "Deathstar", birthday =  "1966-1-02",
                          diagnosis = "other", current_script = "vitamins", current_dose = "3")

        data = {'first_name': patient.first_name, 'last_name': patient.last_name, 'birthday' : patient.birthday,
                'diagnosis' : patient.diagnosis, 'current_script' : patient.current_script,
                'current_dose' : patient.current_dose}

        pform = PatientForm(data)
        assert pform.is_valid()
        #c.post(data)
        #c.post(pform)
        # response = add(request)
        # assert (response.status_code == 200)

    # This is meant to test whether an invalid form will be rejected
    def test_add_invalid(self):
        patient = Patient(first_name="", last_name="")
        data = {'first_name': patient.first_name, 'last_name': patient.last_name, }
        pform = PatientForm(data)
        assert not (pform.is_valid())


    def test_edit(self):
        request = self.factory.get('edit')
        request.user = self.user
        response = edit(request)
        assert (response.status_code == 200)

# Tests code outside Views, but still inside patient folder
class OtherPatientFunctions(unittest.TestCase):
    #This checks to make sure this form is valid
    def test_patient_form(self):
        patient = Patient(first_name = "success", last_name = "test", birthday =  "1966-1-02",
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
    # myTest.test_delete_no_auth()
    # myTest.test_delete()
    # myTest.test_add()
    # myTest.test_add_valid()
    # myTest.test_add_invalid()
    # myTest.test_edit()
    myTest = OtherPatientFunctions()
    myTest.test_patient_form()



main()
