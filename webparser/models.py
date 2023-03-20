from django.db import models
from accounts.models import CustomUser
from options.models import Qualification, Education_base, Speciality, University
from django.core.validators import MinValueValidator

class Template(models.Model):

    name            = models.CharField('Name', max_length=200)
    qualification   = models.ForeignKey(Qualification, on_delete=models.CASCADE)
    education_base  = models.ForeignKey(Education_base, on_delete=models.CASCADE)
    speciality      = models.ManyToManyField(Speciality)
    university      = models.ManyToManyField(University)

    year            = models.IntegerField(
                        validators=[
                            MinValueValidator(2018),
                        ])
    user            = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Report(models.Model):

    template = models.OneToOneField(
        Template,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    institutes_table    = models.BooleanField('Educational institutions ', default=True)
    programs_table      = models.BooleanField('Educational programs of higher education institutions', default=True)
    static_table        = models.BooleanField('Statistical data on higher education institution', default=True)
    summary_table       = models.BooleanField('Summary data by region', default=True)