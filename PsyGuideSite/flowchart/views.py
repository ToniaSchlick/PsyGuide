from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .models import Chart
from .forms import ChartForm
from .xml_reader import load_xml


def viewAllCharts(request):
	return render(request, 'view_all_charts.html', {'flowcharts': Chart.objects.all()})

def viewChart(request):
	pk = request.GET.get('pk')
	if pk:
		flowchart = Chart.objects.get(pk=pk)
		load_xml(pk)
		return render(request, 'view_chart.html', { 'flowchart': flowchart })

# def addChart(request):
# 	form = ChartForm(request.POST or None)
# 	if form.is_valid():
# 		form.save()
# 		return redirect(reverse('flowchart:view_all_charts'))
# 	context = {
# 		'form': form
# 	}
# 	return render (request, 'add_chart.html', context)

def editChart(request):
	pk = request.GET.get('pk')

	if request.method == "POST":
		form = ChartForm(request.POST or None) #, instance=p)
		if form.is_valid():
			# This -1 is to ignore the slash at the end
			pk = pk[:-1]
			p = Chart.objects.get(pk=pk)
			p.name = form.cleaned_data['name']
			p.chart = form.cleaned_data['chart']
			p.save()
			return redirect(reverse('flowchart:view_all_charts'))
	else:
		p = get_object_or_404(Chart, pk=pk)
		form = ChartForm(instance=p)
	context = {'form': form, 'flowchart': Chart.objects.get(pk=pk)}
	return render(request, 'view_all_charts.html', context)

def deleteChart(request):
	if request.user.is_authenticated:
	
		pk = request.GET.get('pk')
		p = Chart.objects.get(pk=pk)
		p.delete()
		return redirect(reverse('flowchart:view_all_charts'))
	else: 
		return render(request,'delete_chart.html')

	if request.method == "POST":
		p.delete()
		return redirect(reverse('flowchart:view_all_charts'))
	else:
		context = {'flowchart': Chart.objects.get(pk=pk)}
		return render(request, 'delete_chart.html', context)
