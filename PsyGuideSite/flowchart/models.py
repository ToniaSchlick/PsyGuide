from django.db import models
from django.conf import settings
import json



# Create your models here.
class Chart(models.Model):
    name = models.CharField(max_length=50, default='')
    img = models.ImageField(null=True)
    chart = models.FileField(null=True)
    
    



