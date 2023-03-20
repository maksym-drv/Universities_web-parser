from django.contrib import admin
from .models import Region, Speciality, Education, Qualification, Education_base

admin.site.register(Education)
admin.site.register(Qualification)
admin.site.register(Education_base)
admin.site.register(Region)
admin.site.register(Speciality)
