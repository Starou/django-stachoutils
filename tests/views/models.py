# -*- coding: utf-8 -*-

from django.db import models


class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.IntegerField()
    purchased_on = models.DateField()
    for_sale = models.BooleanField(default=False)
    last_driver = models.ForeignKey('Person', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "cars/{}/".format(self.pk)

    def price_html(self):
        return u'<em>{}</em>€'.format(self.price)
    price_html.allow_tags = True
    price.short_description = 'price'


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __unicode__(self):
        return self.__str__()
