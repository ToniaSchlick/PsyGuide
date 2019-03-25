# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from patients.models import patient
from patients.forms import PatientForm


# Create your views here.
def algorithms_view(request):
	return render (request, 'prescriber/algorithms.html')

def index(request):
	return render (request, 'prescriber/index.html', {'patients': patient.objects.all()})

def all_patients_view(request):
	return render (request, 'prescriber/patients.html', {'patients': patient.objects.all()})

def patient_detail_view(request):
	pk = request.GET.get('pk')
	if pk:
		return render (request, 'prescriber/viewpatient.html', { 'patient': patient.objects.get(pk=pk) })
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
