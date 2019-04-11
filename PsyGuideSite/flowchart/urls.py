from django.urls import path

from . import views

app_name = 'flowchart'

urlpatterns = [
	path('add_chart/', views.addChart, name = 'add_chart'),
	path('view_all_charts/', views.viewAllCharts, name = 'view_all_charts'),
    path('view_chart/', views.viewChart, name = 'view_chart'),
    path('edit_chart/', views.editChart, name='edit_chart'),
]


	
	
	
	
