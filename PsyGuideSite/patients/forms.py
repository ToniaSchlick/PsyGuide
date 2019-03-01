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
        #TODO: Maybe put this closer to the html
        widgets = {
            "first_name": forms.TextInput(attrs={'class': 'form-control'}),
            "last_name": forms.TextInput(attrs={'class': 'form-control'}),
            "birthday": forms.DateInput(attrs={'class': 'form-control'}),
            "diagnosis": forms.TextInput(attrs={'class': 'form-control'}),
            "current_script": forms.TextInput(attrs={'class': 'form-control'}),
            "current_dose": forms.TextInput(attrs={'class': 'form-control'}),
        }
