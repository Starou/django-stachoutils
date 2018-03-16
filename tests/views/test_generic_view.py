# -*- coding: utf-8 -*-

import datetime
from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django_stachoutils.views import generic
from .actions import sell_cars
from .admin import CarAdmin
from .models import Car


class GenericListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Car.objects.create(brand='Saab', name='9.3', price=12500, purchased_on=datetime.date(2015, 7, 29))
        Car.objects.create(brand='Saab', name='900', price=1800, purchased_on=datetime.date(2001, 3, 29))
        Car.objects.create(brand='Saab', name='9.5', price=23700, purchased_on=datetime.date(2012, 2, 11))
        Car.objects.create(brand='Alfa-Romeo', name='Giullia', price=19500, purchased_on=datetime.date(2014, 7, 12))
        Car.objects.create(brand='Alfa-Romeo', name='Sprint', price=11200, purchased_on=datetime.date(2015, 9, 29))
        Car.objects.create(brand='Subaru', name='Forester', price=34500, purchased_on=datetime.date(2016, 1, 29))
        Car.objects.create(brand='Subaru', name='Impreza', price=11200, purchased_on=datetime.date(2012, 6, 29))

        cls.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def setUp(self):
        self.queryset = Car.objects.all().order_by('brand', 'name')
        self.rf = RequestFactory()

    def test_generic_list(self):
        request = self.rf.get('/cars?page=2')
        request.user = self.user
        columns = [
            {'label': 'Name', 'field': 'name', 'link': {'href': 'get_absolute_url'}},
            {'label': 'Brand', 'field': 'brand'},
            {'label': 'Price', 'field': 'price_html'},
            {'label': 'Purchased Year', 'field': 'purchased_on', 'filters': [('date', 'Y')]},
            {'label': 'For Sale', 'field': 'for_sale'},
        ]
        actions = [sell_cars]
        response = generic.generic_list(request, self.queryset, columns, 'generic_list_test.html',
                                        Car, ClassAdmin=CarAdmin, actions=actions)
        self.assertHTMLEqual(response.content.decode('utf8'), """
            <html>
              <form action="" method="post">
                <div class="actions">
                  <label>Action&nbsp;:
                    <select name="action">
                      <option selected="selected" value="">---------</option>
                      <optgroup label="autres">
                        <option value="sell_cars">Sell the cars</option>
                      </optgroup>
                    </select>
                  </label>
                  <button value="0" name="index" title="Execute the selected action" class="button" type="submit">Execute</button>
                </div>
              </form>
            </html>""")
