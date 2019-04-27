from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from questionnaire.views import *
from questionnaire.models import *
from patient.models import Patient


class TestViewFunctions(TestCase):
    # Set up a logged in user for the tests
    def setUp(self):
        self.factory = RequestFactory()

        User = get_user_model()
        self.user = User.objects.create_user(
            username='jacob',
            password='top_secret'
        )

        self.qInst = Questionnaire.objects.create(name="Questionnaire 1")
        self.pInst = Patient.objects.create(
            first_name="Bob",
            last_name="Loblaw"
        )

    # ** Utility functions must not have test_ as a prefix
    # This is so they aren't called in error by the TestRunner
    def util_test_view(self, viewName, expectedCode, data={}):
        request = self.factory.get(viewName, data)
        request.user = self.user
        response = eval(viewName)(request)
        self.assertEqual(response.status_code, expectedCode)

    def util_test_view_post(self, viewName, expectedCode, data={}):
        request = self.factory.post(viewName, data)
        request.user = self.user
        response = eval(viewName)(request)
        self.assertEqual(response.status_code, expectedCode)

    def test_administer(self):
        self.util_test_view('administer', 200)

        # Test with just patient id
        self.util_test_view('administer', 200, {"ppk": self.pInst.pk})

        # Test with both patient and questionnaire id
        self.util_test_view('administer', 200, {
            "ppk": self.pInst.pk,
            "qpk": self.qInst.pk
        })

        # Test loading of canned response
        file = open("questionnaire/test_data/questionnaire_response_creation.json", "r")
        self.util_test_view_post("administer", 302, {
            "response": file.read(),
            "qpk": self.qInst.pk,
            "ppk": self.pInst.pk
        })

    def test_view(self):
        self.util_test_view('view', 200)

        self.util_test_view('view', 200, {"qpk": self.qInst.pk})

    def test_viewResponse(self):
        self.util_test_view('view_response', 200)

        self.rInst = QuestionnaireResponse.objects.create(
            patient=self.pInst,
            questionnaire=self.qInst,
        )

        self.util_test_view('view_response', 200, {
            "qrpk": self.rInst.pk
        })

    def test_create(self):
        self.util_test_view('create', 200)

        # Load test data and submit it
        file = open("questionnaire/test_data/questionnaire_creation.json", "r")
        self.util_test_view_post("create", 302, {
            "questionnaire": file.read()
        })

    def test_viewAll(self):
        self.util_test_view('view_all', 200)

    def test_edit(self):
        self.util_test_view('edit', 200)

        self.util_test_view('edit', 200, {"qpk": self.qInst.pk})

    def test_delete(self):
        # Delete redirects always with a login
        self.util_test_view('delete', 302)

class TestQuestionnaire(TestCase):
    def setUp(self):
        self.qInst = Questionnaire.objects.create(name="Questionnaire 1")

    def test_addQuestionSet(self):
        # New Questionnaire should have no sets
        self.assertEqual(self.qInst.getQuestionSets().count(), 0)

        self.qInst.addQuestionSet(0, "Quiz", True)

        self.assertEqual(self.qInst.getQuestionSets().count(), 1)

    def test_addScoringFlag(self):
        self.assertEqual(self.qInst.getScoringFlags().count(), 0)

        self.qInst.addScoringFlag("Always True", "1==1", "true")

        self.assertEqual(self.qInst.getScoringFlags().count(), 1)

class TestQuestionSet(TestCase):
    def setUp(self):
        self.qInst = Questionnaire.objects.create(name="Questionnaire 1")
        self.qSet = self.qInst.addQuestionSet(0, "boring topic", False)

    def test_addQuestion(self):
        self.assertEqual(self.qSet.getQuestions().count(), 0)

        self.qSet.addQuestion(0, "Question 1")

        self.assertEqual(self.qSet.getQuestions().count(), 1)

    def test_questionSet_addAnswer(self):
        self.assertEqual(self.qSet.getAnswers().count(), 0)

        self.qSet.addAnswer(0, "Answer 1")

        self.assertEqual(self.qSet.getAnswers().count(), 1)

class TestQuestionnaireResponse(TestCase):
    def setUp(self):
        self.qInst = Questionnaire.objects.create(name="Questionnaire 1")
        self.qSet = self.qInst.addQuestionSet(0, "boring topic", False)
