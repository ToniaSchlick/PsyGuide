# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin

from patient.models import Patient
from questionnaire.models import *
from flowchart.models import Chart, ChartNode 

# Register your models here.
admin.site.site_header = 'PsyGuide Management'
admin.site.register(ChartNode)
admin.site.register(Chart)
admin.site.register(Patient)
admin.site.register(Questionnaire)
admin.site.register(QuestionAnswerSet)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(QuestionnaireResponse)
admin.site.register(QuestionResponse)
admin.site.register(ScoringRange)
