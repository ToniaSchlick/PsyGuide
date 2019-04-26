from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from questionnaire.views import *
from questionnaire.models import *


class TestViewFunctions(TestCase):
    # Set up a logged in user for the tests
    def setUp(self):
        self.factory = RequestFactory()

        User = get_user_model()
        self.user = User.objects.create_user(username='jacob', password='top_secret')

        Questionnaire.objects.create(name="Questionnaire 1")

    # ** Utility functions must not have test_ as a prefix
    # This is so they aren't called in error by the TestRunner
    def util_test_view(self, viewName, expectedCode, data={}):
        request = self.factory.get(view, data)
        request.user = self.user
        response = eval(viewName)(request)
        self.assertEqual(response.status_code, expectedCode)

    # TODO: Test with no auth as well for each view?

    def test_administer(self):
        self.util_test_view('administer', 200)

    def test_view(self):
        self.util_test_view('view', 200)

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
        self.util_test_view('delete', 302)

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
