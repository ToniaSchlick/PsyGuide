# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.urls import reverse, resolve
# Create your tests here.

#test url paths
class TestUrls:

    def test_index_url(self):
        path = reverse('index')
        assert resolve(path).views_name == 'index'
