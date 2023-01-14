from django.contrib import admin
from .models import CustomUser

class UserAdmin(admin.ModelAdmin):
    exclude = ('password', )

admin.site.register(CustomUser, UserAdmin)