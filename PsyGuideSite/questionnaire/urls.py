from django.urls import path

from . import views

app_name = 'questionnaire'

urlpatterns = [
	path('administer/', views.administer, name = 'administer'),
	path('view_response/', views.view_response, name = 'view_response'),
	path('create/', views.create, name = 'create'),
	path('view_all/', views.view_all, name = 'view_all'),
	path('delete/', views.delete, name = 'delete'),
	path('edit/', views.edit, name = 'edit'),
	path('view/', views.view, name = 'view')
]
