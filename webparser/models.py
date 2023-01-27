from json import load
from django.db import models
from django.conf import settings

class Template(models.Model):

    options = {}
    for option in settings.TARGET_OPTIONS:
        with open(f'{settings.OPTIONS_ROOT}{option}.json', 'r') as file:
            options[option] = load(file)

    name            = models.CharField('Name', max_length=200)
    qualification   = models.CharField('Qualification', max_length=200, choices=options['qualifications'])
    education_base  = models.CharField('Education base', max_length=200, choices=options['education_bases'])
    speciality      = models.CharField('Speciality', max_length=200, choices=options['specialities'])
    institution     = models.CharField('Institution', max_length=200, null=True, blank=True)
    region          = models.CharField('Region', max_length=200, null=True, choices=options['regions'], blank=True)
    program         = models.CharField('Program', max_length=200, null=True, blank=True)
    form            = models.CharField('Type', max_length=200, null=True, choices=options['forms'], blank=True)
    course          = models.CharField('Course', max_length=200, null=True, choices=options['courses'], blank=True)

    def __str__(self):
        return self.name