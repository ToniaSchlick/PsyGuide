from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
from django.conf import settings
from flowchart.models import Chart



class Patient(models.Model):

    first_name = models.CharField(max_length=30, default='')
    first_name = models.CharField(max_length=30, default='')
    last_name = models.CharField(max_length=30, default='')
    birthday = models.DateField(null=True, blank=True)
    DIAGNOSIS_CHOICES = (
        ('none', 'none'),
        ('Depression', 'Depression'),
        ('Bipolar Disorder Currently Depressed', 'Bipolar Disorder Currently Depressed'),
        ('Bipolar Disorder Currently Hypomanic/Manic', 'Bipolar Disorder Currently Hypomanic/Manic'),
        ('Mood Disorder', 'Mood Disorder'),
        ('other', 'other'))
    diagnosis = models.CharField(max_length=90, choices = DIAGNOSIS_CHOICES, default='')
    
    # populate the care_plan choice menu
    try:
        plansList = list(Chart.objects.values_list('name', flat=True))
    except:
        plansList = []
    PLAN_CHOICES = list(map(lambda x: (x, x), plansList))          
    care_plan = models.CharField(max_length=90, choices = PLAN_CHOICES, default='')
    current_stage = models.CharField(max_length=30, default='', null=True, blank=True)
    current_script = models.CharField(max_length=30, default='')
    current_dose = models.CharField(max_length=30, default='')
    class Meta:
        ordering = ('last_name', 'first_name',)


