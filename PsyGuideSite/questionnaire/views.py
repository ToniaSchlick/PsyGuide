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
				questionSet_id = questionSetPk
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

		# Find ScoringRange from the score of the response
		scoringRangeInst = ScoringRange.objects.filter(lowerBound__lte=score, upperBound__gte=score)[0]

		#If there's no scoring range, that's fine, just add it if one exists.
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
		return render(request, 'questionnaire/administer.html', context)
	elif ppk:
		context = {
			'patient': Patient.objects.get(pk=ppk),
			'questionnaires': Questionnaire.objects.all()
		}
		return render(request, 'questionnaire/administer.html', context)
	return render(request, 'questionnaire/administer.html')

def viewResponse(request):
	qrpk = request.GET.get('qrpk')
	if qrpk:
		context = {
			'questionnaireResponse': QuestionnaireResponse.objects.get(pk=qrpk)
		}
		return render(request, 'questionnaire/view_response.html', context)
	return render(request, 'questionnaire/view_response.html')

def create(request):
	if request.method == "POST":
		creationJson = json.loads(request.POST.get('questionnaire'))

		# Create root questionnaire instance
		questionnaireInst = Questionnaire.objects.create(
			name=creationJson["name"]
		)

		# Create question sets
		setOrdinal = 0
		for questionSet in creationJson["questionSets"]:
			questionSetInst = QuestionSet.objects.create(
				questionnaire=questionnaireInst,
				ordinal=setOrdinal,
				topic=questionSet["topic"],
				scored=questionSet["scored"]
			)

			# Create questions
			questionOrdinal = 0
			for question in questionSet["questions"]:
				questionInst = Question.objects.create(
					questionSet=questionSetInst,
					ordinal=questionOrdinal,
					text=question
				)

				questionOrdinal += 1

			answerOrdinal = 0
			for answer in questionSet["answers"]:
				answerInst = Answer.objects.create(
					questionSet=questionSetInst,
					ordinal=answerOrdinal,
					text=answer
				)

				answerOrdinal += 1

			setOrdinal += 1

		# Create scoring ranges
		for scoringRange in creationJson["scoringRanges"]:
			ScoringRange.objects.create(
				questionnaire=questionnaireInst,
				lowerBound=scoringRange["lowerBound"],
				upperBound=scoringRange["upperBound"],
				severity=scoringRange["severity"],
				treatment=scoringRange["treatment"]
			)

	return render(request, 'questionnaire/create.html')

def viewAll(request):
	return render(request, 'questionnaire/view_all.html', {"questionnaires": Questionnaire.objects.all()})
