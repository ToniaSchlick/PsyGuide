from django.test import TestCase
from flowchart.views import *


class TestViewFunctions(unittest.TestCase):
    def __init__(self):
        self.factory = RequestFactory()
        try:
            self.user = User.objects.create_user(username='jacob', password='top_secret')
        except:
            self.user = Client()
            self.user.login(username='jacob', password='top_secret')


    def test_view_all_charts(self):
        request = self.factory.get('view_all_charts')
        request.user = self.user
        response = viewAllCharts(request)
        assert (response.status_code == 200)

    def test_view_chart(self):
        request = self.factory.get('view_chart')
        request.user = self.user
        response = viewChart(request)
        assert (response.status_code == 200)

    def test_add_chart(self):
        request = self.factory.get('add_chart')
        request.user = self.user
        response = addChart(request)
        assert (response.status_code == 200)


def main():
    myTest = TestViewFunctions()
    myTest.test_view_all_charts()
    #myTest.test_view_chart()
    myTest.test_add_chart()





main()