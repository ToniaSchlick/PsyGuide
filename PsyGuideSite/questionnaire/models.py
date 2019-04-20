from __future__ import unicode_literals
from django.utils.timezone import now
from django.db import models
from django.conf import settings
from simpleeval import simple_eval

class Questionnaire(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name

class QuestionSet(models.Model):
    questionnaire = models.ForeignKey("Questionnaire", on_delete=models.CASCADE)
    ordinal = models.IntegerField(default=0)
    topic = models.TextField(default="")
    scored = models.BooleanField(default=True)
    def __str__(self):
        return str(self.ordinal) + ": " + self.topic
    class Meta:
        ordering = ('ordinal', )

class ScoringFlag(models.Model):
    questionnaire = models.ForeignKey("Questionnaire", on_delete=models.CASCADE)
    expression = models.TextField(default="")
    title = models.CharField(max_length=30)
    description = models.TextField(default="")

class Question(models.Model):
    questionSet = models.ForeignKey("QuestionSet", on_delete=models.CASCADE)
    ordinal = models.IntegerField(default=0)
    text = models.TextField(default="")
    def __str__(self):
        return str(self.ordinal) + ": " + self.text
    class Meta:
        ordering = ('ordinal', )

class Answer(models.Model):
    questionSet = models.ForeignKey("QuestionSet", on_delete=models.CASCADE)
    ordinal = models.IntegerField(default=0)
    text = models.TextField(default="")
    def __str__(self):
        return str(self.ordinal) + ": " + self.text
    class Meta:
        ordering = ('ordinal', )

class QuestionnaireResponse(models.Model):
    patient = models.ForeignKey("patient.Patient", on_delete=models.CASCADE)
    questionnaire = models.ForeignKey("Questionnaire", on_delete=models.CASCADE)
    date = models.DateTimeField("Date", default=now)

    def getScore(self):
        score = 0
        for setResponse in self.questionsetresponse_set.all():
            score += setResponse.getScore()

        return score

    # Helper method for evaluating scoring flag expressions
    def _getAnswerForQuestion(self, setNum, questionNum):
        # Find the answer to the question "questionNum" in the set "setNum"
        return self.questionsetresponse_set.filter(
            questionSet__ordinal=setNum - 1
        )[0].questionresponse_set.filter(
            question__ordinal=questionNum - 1
        )[0].answer.ordinal

    # Helper method for evaluating scoring flag expressions
    def _getScoreForSet(self, setNum):
        setResponse = self.questionsetresponse_set.filter(
            questionSet__ordinal=setNum - 1
        )[0]

        if setResponse.questionSet.scored:
            return setResponse.getScore()

        return 0

    def getScoringFlags(self):
        caughtFlags = []
        # Get all flags that have a true expression for this response instance
        for flag in self.questionnaire.scoringflag_set.all():
            if simple_eval(
                flag.expression,
                functions={
                    "answer": self._getAnswerForQuestion,
                    "score": self._getScoreForSet
                }):
                caughtFlags.append(flag)

        return caughtFlags

    class Meta:
        ordering = ('-date', )

class QuestionSetResponse(models.Model):
    questionnaireResponse = models.ForeignKey("QuestionnaireResponse", on_delete=models.CASCADE)
    questionSet = models.ForeignKey("QuestionSet", on_delete=models.CASCADE)

    def getScore(self):
        if not self.questionSet.scored:
            return 0

        score = 0
        for questionResponse in self.questionresponse_set.all():
            score += questionResponse.answer.ordinal

        return score


class QuestionResponse(models.Model):
    questionSetResponse = models.ForeignKey("QuestionSetResponse", on_delete=models.CASCADE)
    question = models.ForeignKey("Question", on_delete=models.CASCADE)
    answer = models.ForeignKey("Answer", on_delete=models.CASCADE)
    class Meta:
        ordering = ('question__ordinal', 'answer__ordinal')
