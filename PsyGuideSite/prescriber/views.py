# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PatientForm
from .models import Patient, Questionnaire, QuestionnaireResponse


# Create your views here.

def index(request):
	return render(request, 'prescriber/index.html', {'patients': Patient.objects.all()})

def all_patients_view(request):
	return render(request, 'prescriber/patients.html', {'patients': Patient.objects.all()})


def patient_detail_view(request):
	pk = request.GET.get('pk')
	if pk:
		return render(request, 'prescriber/viewpatient.html', { 'patient': Patient.objects.get(pk=pk) })
	else:
		return render(request, 'prescriber/viewpatient.html')

def patient_form_view(request):
	form = PatientForm(request.POST or None)

	if form.is_valid():
		form.save()
		return HttpResponseRedirect('/patients')
	context = {
		'form': form
	}
	return render (request, 'prescriber/addpatient.html', context)

def patient_take_questionnaire(request):
	# Handle questionnaire response
	if request.method == 'POST':
		patientInst = Patient.objects.get(pk=request.POST.get("ppk"))
		questionnaireInst = Questionnaire.objects.get(pk=request.POST.get("qpk"))
		responseInst = QuestionnaireResponse(patient=patientInst, questionnaire=questionnaireInst, data=request.POST.get("qrData"))
		responseInst.save()
		return render(request, 'prescriber/takequestionnaire.html')

	qpk = request.GET.get('qpk')
	ppk = request.GET.get('ppk')
	if qpk and ppk:
		context = {
			'patient': Patient.objects.get(pk=ppk),
			'questionnaire': Questionnaire.objects.get(pk=qpk)
		}
		return render(request, 'prescriber/takequestionnaire.html', context)
	elif ppk:
		context = {
			'patient': Patient.objects.get(pk=ppk),
			'questionnaires': Questionnaire.objects.all()
		}
		return render(request, 'prescriber/takequestionnaire.html', context)
	return render(request, 'prescriber/takequestionnaire.html')

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)

		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			return redirect('index')
	else:
		form = UserCreationForm()
	context = {'form': form}
	return render(request, 'registration/register.html', context)
