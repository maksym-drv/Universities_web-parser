from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    username    = None
    email       = models.EmailField(('E-mail address'), unique=True)
    
    short_table = models.FileField(null = True)
    static_table = models.FileField(null = True, upload_to='excel_files/')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email