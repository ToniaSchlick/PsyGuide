# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from patients.models import patient
from patients.forms import PatientForm


# Create your views here.

def index(request):
	return render (request, 'prescriber/index.html')

def all_patients_view(request):
	allPatients = patient.objects.all()
	return render (request, 'prescriber/patients.html', {'allPatients': allPatients})

def patient_detail_view(request):
	return render (request, 'prescriber/patient_details.html')

def patient_form_view(request):
	if request.method == 'POST':
		form = PatientForm(request.POST)
		#TODO: logic
	else:
		form = PatientForm()
	return render (request, 'prescriber/addpatient.html', {'form': form})

def phq9_form_view(request):
	return render (request, 'prescriber/phq9_form.html')

def mood_disorder_form_view(request):
	return render (request, 'prescriber/mood_disorder_form.html')

def phq9_model_view(request):
	return render (request, 'prescriber/phq9_model.html')

def mood_disorder_model_view(request):
	return render (request, 'prescriber/mood_disorder_model.html')


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
