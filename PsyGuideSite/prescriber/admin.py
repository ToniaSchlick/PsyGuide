# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Patient, Questionnaire, QuestionnaireResponse

# Register your models here.
admin.site.site_header = 'PsyGuide Management'
admin.site.register(Patient)
admin.site.register(Questionnaire)
admin.site.register(QuestionnaireResponse)
