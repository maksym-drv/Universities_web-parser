from django.contrib import admin
from .models import Region, Speciality, Education, Qualification, Education_base

admin.site.register(Education)

class EducationAdmin(admin.ModelAdmin):
    list_display = ['name', 'registry_id']

admin.site.register(Qualification, EducationAdmin)
admin.site.register(Education_base, EducationAdmin)

admin.site.register(Region)
admin.site.register(Speciality)
