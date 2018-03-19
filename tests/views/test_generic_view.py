# -*- coding: utf-8 -*-

import datetime
from django.contrib.auth.models import User
from django.contrib.messages.storage.base import BaseStorage
from django.test import RequestFactory, TestCase
from django_stachoutils.views import generic
from .actions import sell_cars
from .admin import CarAdmin
from .models import Car, Person


class MessageStorage(BaseStorage):
    """This is a basic messages storage since RequestFactory does not provide
       a complete request object according to settings.MIDDLEWARE.
    """
    def __init__(self, request, *args, **kwargs):
        self.messages = None
        super(MessageStorage, self).__init__(request, *args, **kwargs)

    def _get(self, *args, **kwargs):
        return self.messages, True

    def _store(self, messages, response, *args, **kwargs):
        if messages:
            self.messages = messages
        else:
            self.messages = None
        return []


class BaseGenericListTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.c1 = Car.objects.create(brand='Saab', name='9.3', price=12500, purchased_on=datetime.date(2015, 7, 29))
        cls.c2 = Car.objects.create(brand='Saab', name='900', price=1800, purchased_on=datetime.date(2001, 3, 29))
        cls.c3 = Car.objects.create(brand='Saab', name='9.5', price=23700, purchased_on=datetime.date(2012, 2, 11))
        cls.c4 = Car.objects.create(brand='Alfa-Romeo', name='Giullia', price=19500, purchased_on=datetime.date(2014, 7, 12))
        cls.c5 = Car.objects.create(brand='Alfa-Romeo', name='Sprint', price=11200, purchased_on=datetime.date(2015, 9, 29))
        cls.c6 = Car.objects.create(brand='Subaru', name='Forester', price=34500, purchased_on=datetime.date(2016, 1, 29))
        cls.c7 = Car.objects.create(brand='Subaru', name='Impreza', price=11200, purchased_on=datetime.date(2012, 6, 29))

        cls.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def setUp(self):
        self.queryset = Car.objects.all().order_by('brand', 'name')
        self.rf = RequestFactory()
        self.actions = [sell_cars]
        self.columns = [
            {'label': 'Name', 'field': 'name', 'link': {'href': 'get_absolute_url'}},
            {'label': 'Brand', 'field': 'brand'},
            {'label': 'Price', 'field': 'price_html'},
            {'label': 'Purchased Year', 'field': 'purchased_on', 'filters': [('date', 'Y')]},
            {'label': 'For Sale', 'field': 'for_sale'},
        ]


class UnitTestCase(TestCase):
    def test_set_columns_labels(self):
        columns = [
            {'field': 'name', 'link': {'href': 'get_absolute_url'}},
            {'field': 'brand'},
            {'field': 'price_html'},
            {'field': 'purchased_on', 'filters': [('date', 'Y')]},
            {'field': 'for_sale'},
        ]
        generic.set_columns_labels(Car, columns)
        self.assertEqual([c['label'] for c in columns], [u'name', u'brand', u'Price html', u'purchased on', u'for sale'])

    def test_recursion_in_set_columns_labels(self):
        columns = [
            {'field': 'name', 'link': {'href': 'get_absolute_url'}},
            {'field': 'brand'},
            {'field': 'price_html'},
            {'field': 'purchased_on', 'filters': [('date', 'Y')]},
            {'field': 'for_sale'},
            {
                'with': 'description_by_lang',
                'columns': (
                    {'label': u'Description (Fr)', 'field': 'fr'},  # This should call set_columns_labels() if no label
                    {'label': u'Description (En)', 'field': 'en'},  # is provided but still I can't see a use case...
                )
            },
        ]
        generic.set_columns_labels(Car, columns)


class GenericListTestCase(BaseGenericListTestCase):
    template = 'generic_list_test.html'

    def test_generic_list(self):
        request = self.rf.get('/cars?page=2')
        request.user = self.user
        response = generic.generic_list(request, self.queryset, self.columns, self.template,
                                        Car, ClassAdmin=CarAdmin, actions=self.actions)
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
              <div>
                <div><input type="checkbox" name="_selected_action" value="%(al1)d" />Alfa-Romeo - Giullia</div>
                <div><input type="checkbox" name="_selected_action" value="%(al2)d" />Alfa-Romeo - Sprint</div>
                <div><input type="checkbox" name="_selected_action" value="%(sa1)d" />Saab - 9.3</div>
                <div><input type="checkbox" name="_selected_action" value="%(sa2)d" />Saab - 9.5</div>
                <div><input type="checkbox" name="_selected_action" value="%(sa3)d" />Saab - 900</div>
                <div><input type="checkbox" name="_selected_action" value="%(su1)d" />Subaru - Forester</div>
                <div><input type="checkbox" name="_selected_action" value="%(su2)d" />Subaru - Impreza</div>
              <div>
            </html>""" % {
                'al1': self.c4.pk,
                'al2': self.c5.pk,
                'sa1': self.c1.pk,
                'sa2': self.c3.pk,
                'sa3': self.c2.pk,
                'su1': self.c6.pk,
                'su2': self.c7.pk,
            })

    def test_ordered_generic_list(self):
        request = self.rf.get('/cars?page=2')
        request.user = self.user
        response = generic.generic_list(request, self.queryset, self.columns, self.template,
                                        Car, ClassAdmin=CarAdmin, actions=self.actions,
                                        default_order=['name', 'brand'])
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
              <div>
                <div><input type="checkbox" name="_selected_action" value="%(sa1)d" />Saab - 9.3</div>
                <div><input type="checkbox" name="_selected_action" value="%(sa2)d" />Saab - 9.5</div>
                <div><input type="checkbox" name="_selected_action" value="%(sa3)d" />Saab - 900</div>
                <div><input type="checkbox" name="_selected_action" value="%(su1)d" />Subaru - Forester</div>
                <div><input type="checkbox" name="_selected_action" value="%(al1)d" />Alfa-Romeo - Giullia</div>
                <div><input type="checkbox" name="_selected_action" value="%(su2)d" />Subaru - Impreza</div>
                <div><input type="checkbox" name="_selected_action" value="%(al2)d" />Alfa-Romeo - Sprint</div>
              <div>
            </html>""" % {
                'al1': self.c4.pk,
                'al2': self.c5.pk,
                'sa1': self.c1.pk,
                'sa2': self.c3.pk,
                'sa3': self.c2.pk,
                'su1': self.c6.pk,
                'su2': self.c7.pk,
            })

    def test_generic_list_with_object_list(self):
        request = self.rf.get('/cars?page=2')
        request.user = self.user
        response = generic.generic_list(request, list(self.queryset), self.columns, self.template,
                                        Car, ClassAdmin=CarAdmin, actions=self.actions)
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
              <div>
                <div><input type="checkbox" name="_selected_action" value="%(al1)d" />Alfa-Romeo - Giullia</div>
                <div><input type="checkbox" name="_selected_action" value="%(al2)d" />Alfa-Romeo - Sprint</div>
                <div><input type="checkbox" name="_selected_action" value="%(sa1)d" />Saab - 9.3</div>
                <div><input type="checkbox" name="_selected_action" value="%(sa2)d" />Saab - 9.5</div>
                <div><input type="checkbox" name="_selected_action" value="%(sa3)d" />Saab - 900</div>
                <div><input type="checkbox" name="_selected_action" value="%(su1)d" />Subaru - Forester</div>
                <div><input type="checkbox" name="_selected_action" value="%(su2)d" />Subaru - Impreza</div>
              <div>
            </html>""" % {
                'al1': self.c4.pk,
                'al2': self.c5.pk,
                'sa1': self.c1.pk,
                'sa2': self.c3.pk,
                'sa3': self.c2.pk,
                'su1': self.c6.pk,
                'su2': self.c7.pk,
            })

    def test_filtering_generic_list(self):
        request = self.rf.get('/cars?page=2&q=alfa')
        request.user = self.user
        search = [('Name', 'name__icontains'), ('Brand', 'brand__icontains')]
        response = generic.generic_list(request, self.queryset, self.columns, self.template,
                                        Car, ClassAdmin=CarAdmin, actions=self.actions, search=search)
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
              <div>
                <div><input type="checkbox" name="_selected_action" value="%(al1)d" />Alfa-Romeo - Giullia</div>
                <div><input type="checkbox" name="_selected_action" value="%(al2)d" />Alfa-Romeo - Sprint</div>
              <div>
            </html>""" % {
                'al1': self.c4.pk,
                'al2': self.c5.pk,
            })

    def test_post_without_selected_ation_generic_list(self):
        request = self.rf.post('/cars?page=2', {})
        request.user = self.user
        request._messages = MessageStorage(request)
        response = generic.generic_list(request, self.queryset, self.columns, self.template,
                                        Car, ClassAdmin=CarAdmin, actions=self.actions)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cars?page=2')
        self.assertEqual(list(Car.objects.filter(for_sale=True).order_by('name').values_list('pk', flat=True)),
                         [])

    def test_post_without_selected_items_generic_list(self):
        request = self.rf.post('/cars?page=2', {'action': 'sell_cars'})
        request.user = self.user
        request._messages = MessageStorage(request)
        response = generic.generic_list(request, self.queryset, self.columns, self.template,
                                        Car, ClassAdmin=CarAdmin, actions=self.actions)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cars?page=2')
        self.assertEqual(list(Car.objects.filter(for_sale=True).order_by('name').values_list('pk', flat=True)),
                         [])

    def test_post_generic_list(self):
        request = self.rf.post('/cars?page=2', {'action': 'sell_cars',
                                                '_selected_action': [self.c1.pk, self.c4.pk]})
        request.user = self.user
        response = generic.generic_list(request, self.queryset, self.columns, self.template,
                                        Car, ClassAdmin=CarAdmin, actions=self.actions)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/cars?page=2')
        self.assertEqual(list(Car.objects.filter(for_sale=True).order_by('name').values_list('pk', flat=True)),
                         [self.c1.pk, self.c4.pk])


class GenericListFiltersTestCase(BaseGenericListTestCase):
    template = 'generic_list_filters_test.html'

    @classmethod
    def setUpTestData(cls):
        super(GenericListFiltersTestCase, cls).setUpTestData()
        cls.p1 = Person.objects.create(first_name='Stanislas', last_name='Guerra')
        cls.p2 = Person.objects.create(first_name='Michael', last_name='Schumacher')

    def test_boolean_filters_generic_list(self):
        request = self.rf.get('/cars?page=2')
        request.user = self.user
        filters = [('for_sale', )]
        response = generic.generic_list(request, self.queryset, self.columns, self.template,
                                        Car, ClassAdmin=CarAdmin, actions=self.actions, filters=filters)
        self.assertHTMLEqual(response.content.decode('utf8'), """
            <div>
              <h3><a></a><input type="hidden" name="filter_key" value="for sale" />By for sale</h3>
              <ul>
                <li class="selected"><a href="?">All</a></li>
                <li><a href="?for_sale__exact=1">Oui</a></li>
                <li><a href="?for_sale__exact=0">Non</a></li>
              </ul>
            </div>"""
        )

    def test_fk_filters_generic_list(self):
        request = self.rf.get('/cars?page=2')
        request.user = self.user
        filters = [('last_driver', {
            'choices': Person.objects.all().order_by('last_name'),
            'empty_choice': True,
        })]
        response = generic.generic_list(request, self.queryset, self.columns, self.template,
                                        Car, ClassAdmin=CarAdmin, actions=self.actions, filters=filters)
        self.assertHTMLEqual(response.content.decode('utf8'), """
            <div>
              <h3><a></a><input type="hidden" name="filter_key" value="last driver" />By last driver</h3>
              <ul>
                <li class="selected"><a href="?">All</a></li>
                <li><a href="?last_driver__exact=%d">Stanislas Guerra</a></li>
                <li><a href="?last_driver__exact=%d">Michael Schumacher</a></li>
                <li><a href="?last_driver__isnull=True">Aucun</a></li>
              </ul>
            </div>""" % (self.p1.pk, self.p2.pk)
        )

    def test_fk_filters_filtered_generic_list(self):
        """The url is filtered by one of the filter values."""

        request = self.rf.get('/cars?page=2&last_driver__exact=%d' % self.p2.pk)
        request.user = self.user
        filters = [('last_driver', {
            'choices': Person.objects.all().order_by('last_name'),
            'empty_choice': True,
        })]
        response = generic.generic_list(request, self.queryset, self.columns, self.template,
                                        Car, ClassAdmin=CarAdmin, actions=self.actions, filters=filters)
        self.assertHTMLEqual(response.content.decode('utf8'), """
            <div>
              <h3><a></a><input type="hidden" name="filter_key" value="last driver" />By last driver</h3>
              <ul>
                <li><a href="?">All</a></li>
                <li><a href="?last_driver__exact=%d">Stanislas Guerra</a></li>
                <li class="selected"><a href="?last_driver__exact=%d">Michael Schumacher</a></li>
                <li><a href="?last_driver__exact=%d&last_driver__isnull=True">Aucun</a></li>
              </ul>
            </div>""" % (self.p1.pk, self.p2.pk, self.p2.pk)
        )
