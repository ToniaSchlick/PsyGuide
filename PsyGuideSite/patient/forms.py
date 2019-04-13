from django import forms

from .models import Patient
# from flowchart.models import Chart

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
           ('first_name'),
            'last_name',
            'birthday',
            'diagnosis',
            'care_plan',
            'current_stage',
            'current_script',
            'current_dose'
        ]
