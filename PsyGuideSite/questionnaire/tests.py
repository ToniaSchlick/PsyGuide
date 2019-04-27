from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from questionnaire.views import *
from questionnaire.models import *


class TestViewFunctions(TestCase):
    # Set up a logged in user for the tests
    def setUp(self):
        self.factory = RequestFactory()

        User = get_user_model()
        self.user = User.objects.create_user(username='jacob', password='top_secret')

        self.qInst = Questionnaire.objects.create(name="Questionnaire 1")
        self.pInst = Patient.objects.create()

    # ** Utility functions must not have test_ as a prefix
    # This is so they aren't called in error by the TestRunner
    def util_test_view(self, viewName, expectedCode, data={}):
        request = self.factory.get(viewName, data)
        request.user = self.user
        response = eval(viewName)(request)
        self.assertEqual(response.status_code, expectedCode)

    def util_test_anon_view(self, viewName, expectedCode, data={}):
        request = self.factory.get(viewName, data)
        request.user = AnonymousUser()
        response = eval(viewName)(request)
        self.assertEqual(response.status_code, expectedCode)



    def test_administer(self):
        # No patient of questionnaire
        self.util_test_view('administer', 200)

        # Specify only patient
        self.util_test_view("administer", 200, {
            "ppk": self.pInst.pk
        })

        # Specify both patient and questionnaire
        self.util_test_view("administer", 200, {
            "ppk": self.pInst.pk,
            "qpk": self.qInst.pk
        })

    def test_view(self):
        self.util_test_view('view', 200)

        self.util_test_view('view', 200, {
            "qpk": self.qInst.pk
        })

    def test_viewResponse(self):
        self.util_test_view('view_response', 200)

    def test_create(self):
        self.util_test_view('create', 200)

    def test_viewAll(self):
        self.util_test_view('view_all', 200)

    def test_edit(self):
        self.util_test_view('edit', 200)

    def test_delete(self):
        # Delete redirects always with a login
        self.util_test_view('delete', 302, {
            "qpk": self.qInst.pk
        })

        # Shows please login else
        self.util_test_anon_view('delete', 200, {
            "qpk": self.qInst.pk
        })

class TestQuestionnaireModels(TestCase):
    def setUp(self):
        self.qInst = Questionnaire.objects.create(name="Questionnaire 1")

    def test_questionnaire_addQuestionSet(self):
        # New Questionnaire should have no sets
        self.assertEqual(self.qInst.getQuestionSets().count(), 0)

        self.qInst.addQuestionSet(0, "Quiz", True)

        self.assertEqual(self.qInst.getQuestionSets().count(), 1)

    def test_questionnaire_addScoringFlag(self):
        self.assertEqual(self.qInst.getScoringFlags().count(), 0)

        self.qInst.addScoringFlag("Always True", "1==1", "true")

        self.assertEqual(self.qInst.getScoringFlags().count(), 1)

    def test_questionSet_addQuestion(self):
        # Add a questionSet to add questions to
        set = self.qInst.addQuestionSet(0, "Set 1", True)

        self.assertEqual(set.getQuestions().count(), 0)

        set.addQuestion(0, "Question 1")

        self.assertEqual(set.getQuestions().count(), 1)

    def test_questionSet_addAnswer(self):
        # Add a questionSet to add questions to
        set = self.qInst.addQuestionSet(0, "Set 1", True)

        self.assertEqual(set.getAnswers().count(), 0)

        set.addAnswer(0, "Answer 1")

        self.assertEqual(set.getAnswers().count(), 1)
