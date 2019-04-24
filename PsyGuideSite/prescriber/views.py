# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from patient.models import Patient
from questionnaire.models import Questionnaire, QuestionnaireResponse

def index(request):
	# Get patients in order of their last eval
	unsortedPatients = Patient.objects.all()
	sortedPatients = sorted(unsortedPatients, key= lambda p: -p.getDaysSinceLastEval())
	return render(request, 'prescriber/index.html', {'patients': sortedPatients})

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
