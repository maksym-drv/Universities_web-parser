from .models import Template
from django import forms
from datetime import datetime

class NewTemplateForm(forms.ModelForm):

    year_choices = [(year, year) for year in range(2018, datetime.now().year + 1)]
    year = forms.ChoiceField(choices=year_choices)

    class Meta:
        model = Template
        fields = (
            'name',
            'year',
            'qualification',
            'education_base',
            'speciality'
        )

# class ReportForm(forms.ModelForm):
# 
#     class Meta:
#         model = Report
#         fields = (
#             'institutes_table',
#             'programs_table',
#             'static_table',
#             'summary_table',
#         )