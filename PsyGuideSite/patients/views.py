# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from .models import patien

import patients.QuestionaireLoader as QuestionaireLoader

# Create your views here.

def index(request):
    return render (request, 'patients/index.html', {'questionaires': range(2)})

def questionaire_home(request):
        return index(request)

def questionaire(request, questionaire):
        print(questionaire)
        return render (request, 'questionaires/questionaire.html',
                QuestionaireLoader.load_questionaire(questionaire))



def patient_detail_view(request):
        obj = patient.object.get(id=1)
        return render(request, patient/detail.html, {})
