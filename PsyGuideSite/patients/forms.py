from django import forms

from .models import patient


class PatientForm(forms.modelForm):
    class Meta:
        model = patient
        field = [
            'first_name' 
            'first_last'
            'birthday'
        ]