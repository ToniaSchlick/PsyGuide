from django.db import models
from django.db import models
import json


# ***** this is not right will be changes


# Create your models here.
class Chart(models.Model):
    name = models.CharField(max_length=20),
    chart = ()

# class Action(models.Model):
#     title = models.CharField(max_length=30)
#     stage = models.IntegerField(("stage"))
#     prescription = models.CharField(max_length=30)
#     dose = models.CharField(max_length=30)
#     weeksToNextEval = models.IntegerField(("weeks"))
#     Flowchart = models.ForeignKey(Flowchart, on_delete=models.CASCADE)

# class State(models.Model):
#     description = models.CharField(max_length=100)

# class PossProg(models.Model):
#    title = models.CharField(max_length=30)
#    action = models.CharField(max_length=30)
#    weeksToNextEval = models.IntegerField(("weeks"))
   