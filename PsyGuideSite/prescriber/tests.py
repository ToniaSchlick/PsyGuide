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
        assert (response.status_code == 200)

    #Test a successful form registration
    def test_register(self):
        pass


def main():
    myTest = TestViewFunctions()
    myTest.test_index()
main()