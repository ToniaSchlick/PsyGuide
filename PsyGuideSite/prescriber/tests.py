# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse, resolve
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from prescriber.views import *
#from django.test.testcases import TestCase
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

    #Test a successful form registration
    def test_register(self):
        pass


def main():
    myTest = TestViewFunctions()
    myTest.test_index()
main()