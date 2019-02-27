<<<<<<< HEAD
from django.db import models



=======
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class patient(models.Model):
    first_name = models.CharField("Patient's First Name", max_length=30)
    first_last = models.CharField("Patient's First Last", max_length=30)
    birthday = models.DateField(null=True, blank=True)

    # NONE = 'none'
    # DEPRESSION = 'Depression'
    # BDCD = 'Bipolar Disorder Currently Depressed'
    # BDHMD = 'Bipolar Disorder Currently Hypomanic/Manic'
    # MD = 'Mood Disorder'
    # other = 'other'

    DIAGNOSIS_CHOICES = (
        ('none', 'none'),
        ('Dp', 'Depression'),
        ('BDCD', 'Bipolar Disorder Currently Depressed'),
        ('BDHMD', 'Bipolar Disorder Currently Hypomanic/Manic'),
        ('MD', 'Mood Disorder'),
        ('other', 'other'))
    
    diagnosis = models.CharField(max_length=90, choices = DIAGNOSIS_CHOICES, default='none')
    current_script = models.CharField("Curretn Prescription", max_length=30)
    current_dose = models.CharField("Curretn Dose", max_length=30)

#     current_script = models.ForeignKey(Druglist, on_delete=models.SET_NULL, null=True)
#     current_dose = models.CharField()
>>>>>>> origin/patient
