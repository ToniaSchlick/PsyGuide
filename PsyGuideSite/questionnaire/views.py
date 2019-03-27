from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Questionnaire, QuestionnaireResponse
from patient.models import Patient


def administer(request):
	# Handle questionnaire response
	if request.method == 'POST':
		patientInst = Patient.objects.get(pk=request.POST.get("ppk"))
		questionnaireInst = Questionnaire.objects.get(pk=request.POST.get("qpk"))
        # TODO: Use form?
		responseInst = QuestionnaireResponse(
			patient=patientInst,
			questionnaire=questionnaireInst,
			score=request.POST.get("qrScore"),
			severity=request.POST.get("qrSeverity"),
			treatment=request.POST.get("qrTreatment"),
			data=request.POST.get("qrData")
		)
		responseInst.save()
		return redirect(reverse('questionnaire:view_response') + '?qrpk=' + str(responseInst.pk))

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
