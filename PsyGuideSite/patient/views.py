from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from flowchart.models import Chart
from .models import Patient
from .forms import PatientForm, PatientChartForm
from questionnaire.models import QuestionnaireResponse


def view_all(request):
	return render(request, 'patient/view_all.html', {'patients': Patient.objects.all()})


def view(request):
	pk = request.GET.get('pk')
	if pk:
		patient = Patient.objects.get(pk=pk)
		chartList = Chart.objects.filter(name = patient.care_plan)
		if (patient.chart):
			chart = patient.chart
		elif len(chartList) == 1:
			chart = chartList[0].chart
		else:
			chart = ''
		return render(request, 'patient/view.html', {
			'patient': patient,
			'chart': chart, 
		})
	else:
		return render(request, 'patient/view.html')


def add(request):
	form = PatientForm(request.POST or None)

	if form.is_valid():
		form.save()
		return redirect(reverse('patient:view_all'))
	context = {
		'form': form
	}
	return render (request, 'patient/add.html', context)


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
			p.care_plan = form.cleaned_data['care_plan']
			p.current_stage = form.cleaned_data['current_stage']
			p.current_script = form.cleaned_data['current_script']
			p.current_dose = form.cleaned_data['current_dose']
			p.save()
			return redirect(reverse('patient:view') + '?pk=' + str(pk))
	else:
		p = get_object_or_404(Patient, pk=pk)
		form = PatientForm(instance=p)
	context = {'form': form, 'patient': Patient.objects.get(pk=pk)}
	return render(request, 'patient/edit.html', context)

def edit_chart(request):
	pk = request.GET.get('pk')
	if request.method == "POST":
		form = PatientChartForm(request.POST or None) #, instance=p)
		if form.is_valid():
			pk = pk[:-1]
			p = Patient.objects.get(pk=pk)
			p.xml = form.cleaned_data['xml']
			p.chart = form.cleaned_data['chart']
			p.save()
	else:
		p = get_object_or_404(Patient, pk=pk)
		form = PatientChartForm(instance=p)
	context = {'form': form, 'patient': Patient.objects.get(pk=pk)}
	return render(request, 'patient/view.html', context)

def delete(request):
	if request.user.is_authenticated:
		pk = request.GET.get('pk')
		p = get_object_or_404(Patient, pk=pk)
		p.delete()
		return redirect(reverse('patient:view_all'))
	else:
		return render(request, 'common/please_login_standalone.html')
