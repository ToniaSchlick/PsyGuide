from django.urls import path

from . import views

app_name = 'flowchart'

urlpatterns = [
    path('view/', views.view, name = 'view'),
]
