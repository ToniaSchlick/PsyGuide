# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class patient(models.Model):
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
