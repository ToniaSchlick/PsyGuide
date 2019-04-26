from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from patient.views import *
from patient.forms import *
from patient.models import *

class TestViewFunctions(TestCase):
    # Set up a logged in user for the tests
    def setUp(self):
        self.factory = RequestFactory()

        User = get_user_model()
        self.user = User.objects.create_user(username='jacob', password='top_secret')

    # ** Utility functions must not have test_ as a prefix
    # This is so they aren't called in error by the TestRunner
    def util_test_view(self, viewName, expectedCode, data={}):
        request = self.factory.get(viewName, data)
        request.user = self.user
        response = eval(viewName)(request)
        self.assertEqual(response.status_code, expectedCode)

    # ** Utility functions must not have test_ as a prefix
    # This is so they aren't called in error by the TestRunner
    def util_test_anon_view(self, viewName, expectedCode, data={}):
        request = self.factory.get(viewName, data)
        request.user = self.user
        response = eval(viewName)(request)
        self.assertEqual(response.status_code, expectedCode)


    def test_view_all(self):
        self.util_test_view("view_all", 200)


    def test_view(self):
        self.util_test_view('view', 200)


    # This tests whether code runs through while not being valid, but does not include a form to test submission
    def test_add(self):
        self.util_test_view('add', 200)
        #  https://docs.djangoproject.com/en/2.1/topics/testing/tools/#django.test.Client.post
        # request = self.factory.get('add')
        # request.user = self.user
        # response = add(request)
        # assert (response.status_code == 200)


    # This is meant to test whether a valid form goes through properly. BUT, need to know first if it's possible to
    # add the form to the request, since that's all that the view takes. Doesn't seem possible.
    # https://test-driven-django-development.readthedocs.io/en/latest/05-forms.html   to test forms
    def test_add_valid(self):
        patient = Patient(first_name="success", last_name="add", birthday="1966-1-02", care_plan="Eat pie",pk = 99,
                          diagnosis="Depression", current_script="vitamins", current_dose="3", current_stage="0" )

        data = {'first_name': patient.first_name, 'last_name': patient.last_name, 'birthday': patient.birthday,
                'diagnosis': patient.diagnosis, 'current_script': patient.current_script,
                'current_dose': patient.current_dose, 'care_plan': patient.care_plan,
                'current_stage': patient.current_stage}


        request = self.factory.post('add', data=data)
        response = add(request)
        # Error 302 here because it goes to a redirect instead of a render
        assert (response.status_code == 302)



    def test_delete_no_auth(self):
        self.util_test_anon_view('delete', 200)


    def test_delete(self):
        self.util_test_view('delete', 200)


    def test_edit(self):
        patient = Patient.objects.create(first_name="success", last_name="test", birthday="1966-1-02", care_plan="none",
                                         diagnosis="none", current_script="vitamins", current_dose="3",
                                         current_stage="0", pk=999)
        # print(patient.first_name)

        # Need to put in a pk to edit in order to test the rest of the code
        request = self.factory.get('edit')
        request.user = self.user
        response = edit(request)
        assert (response.status_code == 200)
        patient.delete()

# Tests code outside Views, but still inside patient folder
class OtherPatientFunctions(TestCase):
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
