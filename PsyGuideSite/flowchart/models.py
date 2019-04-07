from django.db import models
from django.conf import settings
import json

starterChart = "hello"


# Create your models here.
class Chart(models.Model):
    global starterChart
    name = models.CharField(max_length=20),
    chart = models.TextField(default= starterChart)



