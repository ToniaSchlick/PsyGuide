from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name = 'index'),
	path('home/', views.index, name = 'index'),
	path('patients/', views.all_patients_view, name = 'patients'),
	path('viewpatient/', views.patient_detail_view, name = 'viewpatient'),
	path('addpatient/', views.patient_form_view, name = 'addpatient'),
	path('phq9_form/', views.phq9_form_view, name = 'phq9_form'),
	path('mood_disorder_form/', views.mood_disorder_form_view, name = 'moodDis_form'),
	path('phq9_mode/l', views.phq9_model_view, name = 'phq9_model'),
	path('mood_disorder_model/', views.mood_disorder_model_view, name = 'moodDis_model'),
	path('register/', views.register, name='register')
]
