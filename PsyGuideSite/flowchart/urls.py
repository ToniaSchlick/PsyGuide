from django.urls import path

from . import views

app_name = 'flowchart'

urlpatterns = [
    path('add_chart/', views.add_chart, name = 'add_chart'),
    path('view_all_charts/', views.view_all_charts, name = 'view_all_charts'),
    path('view_chart/', views.view_chart, name = 'view_chart'),
    path('edit_chart/', views.edit_chart, name='edit_chart'),
    path('parse_xml_string/', views.parse_xml_string, name='parse_xml_string'),
]
