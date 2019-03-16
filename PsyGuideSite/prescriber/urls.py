from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name = 'index'),
	path('home/?', views.index, name = 'index'),
	path('patients/', views.all_patients_view, name = 'patients'),
	path('viewpatient/', views.patient_detail_view, name = 'viewpatient'),
	path('addpatient/', views.patient_form_view, name = 'addpatient'),
	path('register/', views.register, name='register'),
	path('takequestionnaire/', views.patient_take_questionnaire, name='takequestionnaire'),
	path('questionnaireresponse/', views.view_questionnaire_response, name='questionnaireresponse'),
	path('createquestionnaire', views.create_questionnaire, name='createquestionnaire')
]
