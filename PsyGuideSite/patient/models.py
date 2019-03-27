from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
from django.conf import settings

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
