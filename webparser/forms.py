from .models import Template
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