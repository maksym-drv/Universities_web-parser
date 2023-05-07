from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser
from django import forms
 
class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        
        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': "Ім'я",
            'last_name': 'Прізвище',
            'email': 'Електронна пошта',
        }

class UserProfileForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {
            'first_name': "Ім'я",
            'last_name': 'Прізвище',
            'email': 'Електронна пошта',
        }

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput,
                                       label='Поточний пароль')
    new_password = forms.CharField(widget=forms.PasswordInput,
                                   label='Новий пароль')
    confirm_new_password = forms.CharField(widget=forms.PasswordInput,
                                           label='Підтвердити новий пароль')