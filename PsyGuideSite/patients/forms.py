from django import forms

from .models import patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = patient
        fields = [
            'first_name',
            'last_name',
            'birthday',
            'diagnosis',
            'current_script',
            'current_dose'
        ]
