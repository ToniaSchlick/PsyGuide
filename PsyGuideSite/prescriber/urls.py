from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name = 'index'),
	path('patiens', views.all_patiens_view, name = 'patiens'),
	path('patien_detail', views.patien_detail_view, name = 'patien_detail'),
	path('patient_form', views.patient_form_view, name = 'patient_form'),
	path('phq9_form', views.phq9_form_view, name = 'phq9_form'),
	path('mood_disorder_form', views.mood_disorder_form_view, name = 'moodDis_form'),
	path('phq9_model', views.phq9_model_view, name = 'phq9_model'),
	path('mood_disorder_model', views.mood_disorder_model_view, name = 'moodDis_model'),
	path('register', views.register, name='register')	
]