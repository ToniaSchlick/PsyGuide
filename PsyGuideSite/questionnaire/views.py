from django.shortcuts import render, redirect, get_object_or_404
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

		# Store response
		for questionSetPk in responseJson:
			questionSetResponseInst = QuestionSetResponse.objects.create(
				questionnaireResponse = questionnaireResponseInst,
				questionSet_id = questionSetPk
			)

			questionJson = responseJson[questionSetPk]
			for questionPk in questionJson:
				questionResponseInst = QuestionResponse.objects.create(
					questionSetResponse = questionSetResponseInst,
					question_id = questionPk,
					answer_id = questionJson[questionPk]
				)

		return redirect(reverse('questionnaire:view_response') + '?qrpk=' + str(questionnaireResponseInst.pk))

	questionnairePk = request.GET.get('qpk')
	patientPk = request.GET.get('ppk')
	if questionnairePk and patientPk:
		context = {
			'patient': Patient.objects.get(pk=patientPk),
			'questionnaire': Questionnaire.objects.get(pk=questionnairePk)
		}
		return render(request, 'questionnaire/administer.html', context)
	elif patientPk:
		context = {
			'patient': Patient.objects.get(pk=patientPk),
			'questionnaires': Questionnaire.objects.all()
		}
		return render(request, 'questionnaire/administer.html', context)
	return render(request, 'questionnaire/administer.html')

def view(request):
	questionnairePk = request.GET.get('qpk')
	if questionnairePk:
		context = {
			'questionnaire': Questionnaire.objects.get(pk=questionnairePk)
		}
		return render(request, 'questionnaire/view.html', context)
	return render(request, 'questionnaire/view.html')

def viewResponse(request):
	responsePk = request.GET.get('qrpk')
	if responsePk:
		context = {
			'questionnaireResponse': QuestionnaireResponse.objects.get(pk=responsePk)
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

			# Create answers
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
		for scoringFlag in creationJson["scoringFlags"]:
			ScoringFlag.objects.create(
				questionnaire=questionnaireInst,
				expression=scoringFlag["expression"],
				title=scoringFlag["title"],
				description=scoringFlag["description"]
			)

		return redirect(reverse('questionnaire:view_all'))

	return render(request, 'questionnaire/create.html')

def viewAll(request):
	return render(request, 'questionnaire/view_all.html', {"questionnaires": Questionnaire.objects.all()})

def edit(request):
	questionnairePk = request.GET.get('qpk')
	if questionnairePk:
		return render(request, 'questionnaire/edit.html', {"questionnaire": Questionnaire.objects.get(pk=questionnairePk)})

	return render(request, 'questionnaire/edit.html')

def delete(request):
	if request.user.is_authenticated:
		questionnairePk = request.GET.get('qpk')
		questionnaireInst = get_object_or_404(Questionnaire, pk=questionnairePk)
		questionnaireInst.delete()

		return redirect(reverse('questionnaire:view_all'))
	else:
		return render(request, 'common/please_login_standalone.html')
