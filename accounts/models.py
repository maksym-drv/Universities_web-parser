from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, UserManager

class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)

        user = self.model(
            email           = email,
            is_staff        = is_staff,
            is_active       = True, 
            is_superuser    = is_superuser,
            date_joined     = timezone.now(),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True, **extra_fields)

class CustomUser(AbstractUser):
    
    objects = CustomUserManager()

    username    = None
    email       = models.EmailField(('E-mail address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email