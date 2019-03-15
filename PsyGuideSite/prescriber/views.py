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

	# pk = request.GET.get('pk')
	#
	# if request.method == "POST":
	#
	# 	form = PatientForm(request.POST or None, instance=pk)
	# 	if form.is_valid():
	# 		form.save()
	# else:
	# 	form = PatientForm(instance=pk)
	# context = {'form':form,'pk':pk}
	# return render(request, 'prescriber/editpatient.html',context)


	# https://www.youtube.com/watch?v=bKM51uCW6Ic  for reference, 3:14
	pk = request.GET.get('pk')
	form = PatientForm(request.POST or None)

	# Should always be a pk, so long as edit was clicked from looking at patient details
	if pk:
		if form.is_valid():
			#pk.first_name = "Carla"
			form.save()
			# Now sending over pk and
			return render(request, 'prescriber/editpatient.html', {'patient': patient.objects.get(pk=pk)})
			#return HttpResponseRedirect('/patients')

	if pk:
		context = {'form': form}
		#pk.first_name = "Carla"
		form.save()
		#return render (request, 'prescriber/editpatient.html', context)
		# I am assuming this method can take all 4 parameters here
		return render(request, 'prescriber/editpatient.html', context, {'patient': patient.objects.get(pk=pk)})

	return HttpResponseRedirect('/patients')

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
