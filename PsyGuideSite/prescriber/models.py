# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.

class Patient(models.Model):
    first_name = models.CharField(max_length=30, default='N/A')
    first_name = models.CharField(max_length=30, default='N/A')
    last_name = models.CharField(max_length=30, default='N/A')
    birthday = models.DateField(null=True, blank=True)
    DIAGNOSIS_CHOICES = (
        ('none', 'none'),
        ('Dp', 'Depression'),
        ('BDCD', 'Bipolar Disorder Currently Depressed'),
        ('BDHMD', 'Bipolar Disorder Currently Hypomanic/Manic'),
        ('MD', 'Mood Disorder'),
        ('other', 'other'))
    diagnosis = models.CharField(max_length=90, choices = DIAGNOSIS_CHOICES, default='none')
    current_script = models.CharField(max_length=30, default='none')
    current_dose = models.CharField(max_length=30, default='0')
    class Meta:
        ordering = ('last_name', 'first_name',)


class Questionnaire(models.Model):
    name = models.CharField(max_length=30)
    data = models.TextField() # JSON data really, keep it generic though

class QuestionnaireResponse(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    questionnaire = models.ForeignKey("Questionnaire", on_delete=models.CASCADE)
    data = models.TextField() # JSON data
