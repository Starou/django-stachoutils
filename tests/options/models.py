from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CarOption(models.Model):
    car = models.ForeignKey('Car', on_delete=models.CASCADE)
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name
