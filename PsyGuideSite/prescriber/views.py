# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from patients.models import patient
from patients.forms import PatientForm


# Create your views here.

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


def patient_edit_view(request):
	#https://stackoverflow.com/questions/6023421/how-to-edit-model-data-using-django-forms   for pk and lower line
	pk = request.GET.get('pk')
	#post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		# It's not clear what this user creation form is, but I'll assume it's what's supposed to be here
		#form = UserCreationForm(request.POST)
		form = PatientForm(instance = pk)
		if form.is_valid():
			# I'm not sure what these different things are referring to, but I'll put in the stuff from the patient form
			# These are filled in automatically to start with right?
			fname = form.cleaned_data['first_name']
			lname = form.cleaned_data['last_name']
			birthday = form.cleaned_data['birthday']
			diagnosis = form.cleaned_data['diagnosis']
			script = form.cleaned_data['current_script']
			dose = form.cleaned_data['current_dose']

			# Now we just need to save this to the database
			form.save()

			# I believe this needs this pk, right?
			return render(request,'prescriber/editpatient.html',{ 'patient': patient.objects.get(pk=pk) })
	else:
		form = UserCreationForm()
	context = {'form': form}
	return render(request, 'prescriber/editpatient.html', context)


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
