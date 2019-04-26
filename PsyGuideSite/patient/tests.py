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
class TestViewFunctions():  #unittest.TestCase):
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


    def test_function_auth(self, name):
        request = self.factory.get(str(name))
        request.user = AnonymousUser()
        response = eval(name)(request)
        assert (response.status_code == 200)

    # Does not use test function because url name does not match function name
    def test_view_all(self):
        request = self.factory.get('view_all')
        request.user = self.user
        response = viewAll(request)
        assert (response.status_code == 200)


    def test_view(self):
        self.test_function('view')

    # This tests whether code runs through while not being valid, but does not include a form to test submission
    def test_add(self):
        self.test_function('add')
        #  https://docs.djangoproject.com/en/2.1/topics/testing/tools/#django.test.Client.post

        #
        # request = self.factory.get('add')
        # request.user = self.user
        # response = add(request)
        # assert (response.status_code == 200)


    # This is meant to test whether a valid form goes through properly. BUT, need to know first if it's possible to
    # add the form to the request, since that's all that the view takes. Doesn't seem possible.
    # https://test-driven-django-development.readthedocs.io/en/latest/05-forms.html   to test forms
    def test_add_valid(self):
        patient = Patient(first_name="success", last_name="add", birthday="1966-1-02", care_plan="Eat pie",
                          diagnosis="Depression", current_script="vitamins", current_dose="3", current_stage="0",
                          pk = 999)

        data = {'first_name': patient.first_name, 'last_name': patient.last_name, 'birthday': patient.birthday,
                'diagnosis': patient.diagnosis, 'current_script': patient.current_script,
                'current_dose': patient.current_dose, 'care_plan': patient.care_plan,
                'current_stage': patient.current_stage}

        # Creates a filled out form with the above data
        pform = PatientForm(data)
        request = self.factory.post('add', pform)
        request.user = self.user
        response = add(request)

        added = Patient.objects.get(pk=999)
        # Assert that the patient was successfully added
        assert (added == patient)
        # Assert that the response was handled gracefully
        assert (response.status_code == 200)
        # Remove added patient
        added.delete()


    def test_delete_no_auth(self):
        self.test_function_auth('delete')


    def test_delete(self):
        self.test_function('delete')


    def test_edit(self):
        patient = Patient.objects.create(first_name="success", last_name="test", birthday="1966-1-02", care_plan="none",
                          diagnosis="none", current_script="vitamins", current_dose="3", current_stage="0", pk = 999)

        #Need to put in a pk to edit in order to test the rest of the code
        request = self.factory.get('edit')

        request.user = self.user
        response = edit(request)
        assert (response.status_code == 200)
        patient.delete()

# Tests code outside Views, but still inside patient folder
class OtherPatientFunctions(unittest.TestCase):
    #This checks to make sure this form is valid
    def test_patient_form(self):
        patient = Patient(first_name = "success", last_name = "test", birthday =  "1966-1-02", care_plan = "none",
                            diagnosis = "none", current_script = "vitamins", current_dose = "3", current_stage = "0")
        data = {'first_name': patient.first_name, 'last_name': patient.last_name, 'birthday' : patient.birthday,
                'diagnosis' : patient.diagnosis, 'current_script' : patient.current_script,
                'current_dose' : patient.current_dose, 'care_plan' : patient.care_plan,
                'current_stage' : patient.current_stage}
        pform = PatientForm(data)
        assert (pform.is_valid())

    def test_patient_form_invalid(self):
        patient = Patient(first_name="", last_name="", birthday="1966-1-02", care_plan="none",
                          diagnosis="none", current_script="vitamins", current_dose="3", current_stage="0")
        data = {'first_name': patient.first_name, 'last_name': patient.last_name, 'birthday': patient.birthday,
                'diagnosis': patient.diagnosis, 'current_script': patient.current_script,
                'current_dose': patient.current_dose, 'care_plan': patient.care_plan,
                'current_stage': patient.current_stage}
        pform = PatientForm(data)
        assert not (pform.is_valid())


def main():
    myTest = TestViewFunctions()
    myTest.test_view_all()
    myTest.test_view()
    myTest.test_add()
#     myTest.test_add_valid()
    # #myTest.test_delete_no_auth()
    # #myTest.test_delete()
    # #myTest.test_edit()
    #
    # myTest = OtherPatientFunctions()
    # myTest.test_patient_form()
    # myTest.test_patient_form_invalid()



main()
