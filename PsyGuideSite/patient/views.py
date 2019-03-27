from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Patient
from .forms import PatientForm
from questionnaire.models import QuestionnaireResponse


def viewAll(request):
	return render(request, 'view_all.html', {'patients': Patient.objects.all()})

def view(request):
	pk = request.GET.get('pk')
	if pk:
		patient = Patient.objects.get(pk=pk)
		try:
			# Try to get all questionnaires this patient has taken
			questionnaireResponses = QuestionnaireResponse.objects.filter(patient=patient)
		except QuestionnaireResponse.DoesNotExist:
			questionnaireResponses = None
		return render(request, 'view.html', { 'patient': patient, 'questionnaireResponses': questionnaireResponses })
	else:
		return render(request, 'view.html')

def add(request):
	form = PatientForm(request.POST or None)

	if form.is_valid():
		form.save()
		return redirect(reverse('patient:view_all'))
	context = {
		'form': form
	}
	return render (request, 'add.html', context)
