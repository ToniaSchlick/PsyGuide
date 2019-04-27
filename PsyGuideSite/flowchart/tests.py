from django.test import RequestFactory, TestCase
from django.contrib.auth import get_user_model
from flowchart.views import *
from flowchart.models import *
import flowchart.xml_reader as xml_reader


class TestViewFunctions(TestCase):
    # Set up a logged in user for the tests
    def setUp(self):
        self.factory = RequestFactory()

        User = get_user_model()
        self.user = User.objects.create_user(username='jacob', password='top_secret')
    """
    # ** Utility functions must not have test_ as a prefix
    # This is so they aren't called in error by the TestRunner
    def util_test_view(self, viewName, expectedCode, data={}):
        request = self.factory.get(viewName, data)
        request.user = self.user
        response = eval(viewName)(request)
        self.assertEqual(response.status_code, expectedCode)

    def test_view_all_charts(self):
        self.util_test_view("view_all_charts", 200)

    def test_view_chart(self):
        self.util_test_view("view_chart", 200)

    def test_add_chart(self):
        self.util_test_view("add_chart", 200)

    def test_edit_chart(self):
        self.util_test_view("edit_chart", 200)
    """
    def test_parse_xml_string(self):
        string = open("flowchart/test_flowchart", "r").read()
        nodes = xml_reader.load_xml(string)
        self.assertEquals(nodes["8lN2DDwWbF6R6yw3bK0Q-1"].get_content(), "Node1")
        self.assertEquals(nodes["8lN2DDwWbF6R6yw3bK0Q-1"].get_id(), "8lN2DDwWbF6R6yw3bK0Q-1")
        self.assertEquals(nodes["8lN2DDwWbF6R6yw3bK0Q-1"].get_children()[0], "8lN2DDwWbF6R6yw3bK0Q-2")
        self.assertEquals(nodes["8lN2DDwWbF6R6yw3bK0Q-2"].get_parents()[0], "8lN2DDwWbF6R6yw3bK0Q-1")
