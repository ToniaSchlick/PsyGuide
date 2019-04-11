from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
from django.conf import settings

class Questionnaire(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class ScoringRange(models.Model):
    questionnaire = models.ForeignKey("Questionnaire", on_delete=models.CASCADE)
    lowerBound = models.IntegerField(default=0)
    upperBound = models.IntegerField(default=0)
    severity = models.CharField(max_length=30)
    treatment = models.TextField(default="")

class QuestionAnswerSet(models.Model):
    questionnaire = models.ForeignKey("Questionnaire", on_delete=models.CASCADE)
    ordinal = models.IntegerField(default=0)
    topic = models.TextField(default="")
    scored = models.BooleanField(default=True)
    def __str__(self):
        return self.topic
    class Meta:
        ordering = ('ordinal', )

class Question(models.Model):
    questionAnswerSet = models.ForeignKey("QuestionAnswerSet", on_delete=models.CASCADE)
    ordinal = models.IntegerField(default=0)
    text = models.TextField(default="")
    def __str__(self):
        return self.text
    class Meta:
        ordering = ('ordinal', )

class Answer(models.Model):
    questionAnswerSet = models.ForeignKey("QuestionAnswerSet", on_delete=models.CASCADE)
    ordinal = models.IntegerField(default=0)
    text = models.TextField(default="")
    def __str__(self):
        return self.text
    class Meta:
        ordering = ('ordinal', )

class QuestionnaireResponse(models.Model):
    patient = models.ForeignKey("patient.Patient", on_delete=models.CASCADE)
    questionnaire = models.ForeignKey("Questionnaire", on_delete=models.CASCADE)
    date = models.DateTimeField("Date", default=now)
    score = models.IntegerField(default=0)
    scoringRange = models.ForeignKey("ScoringRange", on_delete=models.CASCADE, blank=True, null=True)
    class Meta:
        ordering = ('-date', )

class QuestionAnswerSetResponse(models.Model):
    questionnaireResponse = models.ForeignKey("QuestionnaireResponse", on_delete=models.CASCADE)
    questionAnswerSet = models.ForeignKey("QuestionAnswerSet", on_delete=models.CASCADE)

class QuestionResponse(models.Model):
    questionAnswerSetResponse = models.ForeignKey("QuestionAnswerSetResponse", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    answer = models.ForeignKey("Answer", on_delete=models.CASCADE)
    class Meta:
        ordering = ('question__ordinal', 'answer__ordinal')
