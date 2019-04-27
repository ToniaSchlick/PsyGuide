from django.db import models
from django.conf import settings
import json



# Create your models here.
class Chart(models.Model):
    name = models.CharField(max_length=50, default='')
    xml = models.TextField(null = True, blank=True)
    chart = models.TextField(null=True, blank=True)

class Child(models.Model):
    parent = models.ForeignKey("ChartNode", on_delete=models.CASCADE)

class ChartNode(models.Model):
    nodeId = models.TextField()
    content = models.TimeField()
    # parent = models.ListField()
    # child = models.ListField()
    plan = models.TextField()
