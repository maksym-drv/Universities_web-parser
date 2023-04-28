from django.db import models
from django.core.validators import MinValueValidator
from accounts.models import CustomUser
from webparser.options.models import Qualification, \
    Education_base, Speciality, University

class Template(models.Model):

    name            = models.CharField('Name', max_length=200)
    year            = models.IntegerField(validators=[
                        MinValueValidator(2021), ])
    qualification   = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    education_base  = models.ForeignKey(Education_base, on_delete=models.CASCADE)
    speciality      = models.ManyToManyField(Speciality)
    university      = models.ManyToManyField(University)
    
    short_table     = models.FileField(null = True)
    static_table    = models.FileField(null = True)

    user            = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
