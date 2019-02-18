from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey('Person', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Person(models.Model):
    name = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(choices=[('male', 'Male'), ('female', 'Female')], max_length=6)
