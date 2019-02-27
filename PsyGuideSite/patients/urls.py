from django.conf.urls import url
from . import views

urlpatterns = [
	    url(r'^$', views.index, name = 'Patients'),
            url(r'^questionaire$', views.questionaire_home, name = 'Questionare'),
            url(r'^questionaire/([\w\-]+)$', views.questionaire),
        ]
