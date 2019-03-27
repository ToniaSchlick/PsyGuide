from django.shortcuts import render, redirect, get_object_or_404
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

def edit(request):
	pk = request.GET.get('pk')

	if request.method == "POST":
		form = PatientForm(request.POST or None) #, instance=p)
		if form.is_valid():
			# This -1 is to ignore the slash at the end
			pk = pk[:-1]
			p = Patient.objects.get(pk=pk)
			p.first_name = form.cleaned_data['first_name']
			p.last_name = form.cleaned_data['last_name']
			p.birthday = form.cleaned_data['birthday']
			p.diagnosis = form.cleaned_data['diagnosis']
			p.current_script = form.cleaned_data['current_script']
			p.current_dose = form.cleaned_data['current_dose']
			p.save()
			#form.save()
			return redirect(reverse('patient:view') + '?pk=' + str(pk))
			#return render(request, 'view.html', {'patient': Patient.objects.get(pk=pk)})
			#return HttpResponseRedirect('/patients')
	else:
		p = get_object_or_404(Patient, pk=pk)
		form = PatientForm(instance=p)
	context = {'form': form, 'patient': Patient.objects.get(pk=pk)}
	return render(request, 'edit.html', context)

def delete(request):
	pk = request.GET.get('pk')
	p = Patient.objects.get(pk=pk)
	p.delete()
	return redirect(reverse('patient:view_all'))
