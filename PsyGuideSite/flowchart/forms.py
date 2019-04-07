from django import forms
from .models import Chart


class ChartForm(forms.ModelForm):
    name = form.CharField()

    class Meta:
        model = Chart
        fields = ['name',  'chart']
