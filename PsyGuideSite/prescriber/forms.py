from django import forms

from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
           ('first_name'),
            'last_name',
            'birthday',
            'diagnosis',
            'current_script',
            'current_dose'
        ]
