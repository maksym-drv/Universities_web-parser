from django.db import models

class Region(models.Model):
    name = models.CharField('Name', max_length = 50, unique=True)
    registry_id = models.CharField(max_length = 10, unique=True)

    def __str__(self) -> str:
        return self.name


class Speciality(models.Model):
    name = models.CharField('Name', max_length = 100, unique=True)
    registry_id = models.CharField(max_length = 10, unique=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name_plural = "Specialties"


class Education(models.Model):
    name = models.CharField('Name', max_length = 50, unique=True)

    def __str__(self) -> str:
        return self.name


class Qualification(models.Model):
    name = models.OneToOneField(Education, on_delete=models.CASCADE)
    registry_id = models.CharField(max_length = 10, unique=True)

    def __str__(self) -> str:
        return self.name.name


class Education_base(models.Model):
    name = models.OneToOneField(Education, on_delete=models.CASCADE)
    registry_id = models.CharField(max_length = 10, unique=True)

    def __str__(self) -> str:
        return self.name.name
    

class University(models.Model):
    registry_id = models.CharField(max_length = 10, unique=True)