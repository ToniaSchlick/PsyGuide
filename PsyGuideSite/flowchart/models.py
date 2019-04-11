from django.db import models
from django.conf import settings
import json



# Create your models here.
class Chart(models.Model):
    name = models.CharField(max_length=50, default='')
    xml = models.TextField(null = True)
    chart = models.TextField(null=True)
    
    



