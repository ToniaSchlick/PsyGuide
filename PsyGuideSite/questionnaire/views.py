from django.shortcuts import render, redirect
from django.urls import reverse
import json

from .models import *
from patient.models import Patient


def administer(request):
	# Handle questionnaire response
	if request.method == 'POST':
		patientPk = request.POST.get("ppk")
		questionnairePk = request.POST.get("qpk")

		questionnaireResponseInst = QuestionnaireResponse.objects.create(
			patient_id = patientPk,
			questionnaire_id = questionnairePk
		)
        # Get response array back from post.
		responseJson = json.loads(request.POST.get('response'))["response"]

		# Score and store response
		score = 0
		for questionSetPk in responseJson:
			questionSetResponseInst = QuestionSetResponse.objects.create(
				questionnaireResponse = questionnaireResponseInst,
				questionAnswerSet_id = questionSetPk
			)
			questionJson = responseJson[questionSetPk]
			for questionPk in questionJson:
				answer = Answer.objects.get(pk=questionJson[questionPk])
				questionResponseInst = QuestionResponse.objects.create(
					questionSetResponse = questionSetResponseInst,
					question_id = questionPk,
					answer = answer
				)
				if answer.questionSet.scored:
					score += answer.ordinal


		questionnaireResponseInst.score = score

		# Find ScoringRange
		scoringRangeInst = ScoringRange.objects.filter(lowerBound__lte=score, upperBound__gte=score)[0]

		if scoringRangeInst:
			questionnaireResponseInst.scoringRange = scoringRangeInst
			questionnaireResponseInst.save()

		questionnaireResponseInst.score = score

		return redirect(reverse('questionnaire:view_response') + '?qrpk=' + str(questionnaireResponseInst.pk))

	qpk = request.GET.get('qpk')
	ppk = request.GET.get('ppk')
	if qpk and ppk:
		context = {
			'patient': Patient.objects.get(pk=ppk),
			'questionnaire': Questionnaire.objects.get(pk=qpk)
		}
		return render(request, 'administer.html', context)
	elif ppk:
		context = {
			'patient': Patient.objects.get(pk=ppk),
			'questionnaires': Questionnaire.objects.all()
		}
		return render(request, 'administer.html', context)
	return render(request, 'administer.html')

def viewResponse(request):
	qrpk = request.GET.get('qrpk')
	if qrpk:
		context = {
			'questionnaireResponse': QuestionnaireResponse.objects.get(pk=qrpk)
		}
		return render(request, 'view_response.html', context)
	return render(request, 'view_response.html')

def create(request):
	return render(request, 'create.html')
