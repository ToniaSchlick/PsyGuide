from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
from django.conf import settings

class Questionnaire(models.Model):
    name = models.CharField(max_length=30)
    data = models.TextField(default="") # JSON data really, keep it generic though

class QuestionnaireResponse(models.Model):
    patient = models.ForeignKey("patient.Patient", on_delete=models.CASCADE)
    questionnaire = models.ForeignKey("Questionnaire", on_delete=models.CASCADE)
    date = models.DateTimeField("Date", default=now)
    score = models.IntegerField(default=0)
    severity = models.CharField(max_length=30, default="")
    treatment = models.TextField(default="")
    data = models.TextField(default="") # JSON data
    class Meta:
        ordering = ('-date', )
