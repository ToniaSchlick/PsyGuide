# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.timezone import now

from django.db import models
from django.conf import settings

# Create your models here.

class Patient(models.Model):
    first_name = models.CharField(max_length=30, default='')
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    birthday = models.DateField(null=True, blank=True)
    DIAGNOSIS_CHOICES = (
        ('none', 'none'),
        ('Dp', 'Depression'),
        ('BDCD', 'Bipolar Disorder Currently Depressed'),
        ('BDHMD', 'Bipolar Disorder Currently Hypomanic/Manic'),
        ('MD', 'Mood Disorder'),
        ('other', 'other'))
    diagnosis = models.CharField(max_length=90, choices = DIAGNOSIS_CHOICES, default='')
    current_script = models.CharField(max_length=30, default='')
    current_dose = models.CharField(max_length=30, default='')
    class Meta:
        ordering = ('last_name', 'first_name',)


class Questionnaire(models.Model):
    name = models.CharField(max_length=30)
    data = models.TextField(default="") # JSON data really, keep it generic though

class QuestionnaireResponse(models.Model):
    patient = models.ForeignKey("Patient", on_delete=models.CASCADE)
    questionnaire = models.ForeignKey("Questionnaire", on_delete=models.CASCADE)
    date = models.DateTimeField("Date", default=now)
    score = models.IntegerField(default=0)
    severity = models.CharField(max_length=30, default="")
    treatment = models.TextField(default="")
    data = models.TextField(default="") # JSON data
    class Meta:
        ordering = ('-date', )
