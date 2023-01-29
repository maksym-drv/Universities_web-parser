from .models import Template, Report
from django import forms


class NewTemplateForm(forms.ModelForm):

    class Meta:
        model = Template
        fields = (
            'name',
            'qualification',
            'education_base',
            'speciality',
            'institution',
            'region',
            'program',
            'form',
            'course',        
        )


class ReportForm(forms.ModelForm):

    class Meta:
        model = Report
        fields = (
            'institutes_table',
            'programs_table',
            'static_table',
            'summary_table',
        )