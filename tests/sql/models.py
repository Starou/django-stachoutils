from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    horsepower = models.IntegerField()
    weight = models.IntegerField()
    top_speed = models.IntegerField()
    sales = models.IntegerField()

    def __str__(self):
        return self.name
