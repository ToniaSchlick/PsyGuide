from django.db import models
from django.conf import settings
import json



# Create your models here.
class Chart(models.Model):
    name = models.CharField(max_length=50, default='')
    xml = models.TextField(null = True)
    chart = models.TextField(null=True)
    
class Plan(models.Model):
    name = models.TextField()
    
class Node:
    id = models.TextField()
    content = models.TimeField()
    parent = models.ManyToManyField('self')
    child = models.ManyToManyField('self')
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

   



