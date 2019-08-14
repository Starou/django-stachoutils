# -*- coding: utf-8 -*-

import datetime
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.storage.base import BaseStorage
from django.test import RequestFactory, TestCase
from django_stachoutils.views import generic
from .actions import sell_cars
from .admin import CarAdmin
from .models import Car, Company, Garage, Person


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


class BaseGenericListTest(TestCase):
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


class UnitTest(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.columns = [
            {'field': 'name', 'link': {'href': 'get_absolute_url'}, 'ordering': ['brand', 'name']},
            {'field': 'brand'},
            {'field': 'price_html'},
            {'field': 'purchased_on', 'filters': [('date', 'Y')]},
            {'field': 'for_sale'},
        ]

    def test_set_columns_labels(self):
        generic.set_columns_labels(Car, self.columns)
        self.assertEqual([c['label'] for c in self.columns],
                         [u'name', u'brand', u'price', u'purchased on', u'for sale'])

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

    def test_get_ordering_params(self):
        request = self.rf.get('/cars?page=2&o=1&ot=asc')  # Order by Brand
        ordering = generic.get_ordering_params(request, Car, self.columns, default_order=None)
        self.assertEqual(ordering, ['brand'])

        request = self.rf.get('/cars?page=2&o=1&ot=desc')  # Descending order
        ordering = generic.get_ordering_params(request, Car, self.columns, default_order=None)
        self.assertEqual(ordering, ['-brand'])

    def test_get_ordering_params_by_method(self):
        request = self.rf.get('/cars?page=2&o=2&ot=asc')  # Order by Price, then name (price_html method)
        ordering = generic.get_ordering_params(request, Car, self.columns, default_order=None)
        self.assertEqual(ordering, ['price', 'name'])

        request = self.rf.get('/cars?page=2&o=2&ot=desc')  # Descending order
        ordering = generic.get_ordering_params(request, Car, self.columns, default_order=None)
        self.assertEqual(ordering, ['-price', '-name'])

    def test_get_ordering_params_default(self):
        request = self.rf.get('/cars?page=2')
        ordering = generic.get_ordering_params(request, Car, self.columns, default_order='name')
        self.assertEqual(ordering, 'name')

    def test_get_ordering_params_with_ordering_set_in_column(self):
        request = self.rf.get('/cars?page=2&o=0&ot=asc')  # Order by name
        ordering = generic.get_ordering_params(request, Car, self.columns, default_order=None)
        self.assertEqual(ordering, ['brand', 'name'])

        request = self.rf.get('/cars?page=2&o=0&ot=desc')  # Descending
        ordering = generic.get_ordering_params(request, Car, self.columns, default_order=None)
        self.assertEqual(ordering, ['-brand', '-name'])

    def test_has_column_perm(self):
        user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        col = {'field': 'purchased_on',
               'perms': ['views.see_car_purchased_on']}
        self.assertFalse(generic.has_column_perm(user, col))

        # Add the permission to the user
        car_content_type = ContentType.objects.get_for_model(Car)
        perm = Permission.objects.create(name="Can see puchased on date of a car",
                                         content_type=car_content_type,
                                         codename='see_car_purchased_on')
        user.user_permissions.add(perm)
        user = User.objects.get(pk=user.pk)
        self.assertTrue(generic.has_column_perm(user, col))

        # Test the 'not' operator
        col = {'field': 'price',
               'perms': ['!views.see_car_purchased_on']}
        self.assertFalse(generic.has_column_perm(user, col))

    def test_get_filter(self):
        current_filters = {'brand': 'Saab'}

        filter_1 = ('for_sale', )
        self.assertEqual(generic.get_filter(Car, current_filters, filter_1), (
            u'for sale', [
                ('brand=Saab', u'All', True),
                ('brand=Saab&for_sale__exact=1', 'Oui', False),
                ('brand=Saab&for_sale__exact=0', 'Non', False)
            ]
        ))

    def test_get_filter_fk(self):
        current_filters = {'brand': 'Saab'}

        Company.objects.create(name='Thomson Reuters')
        Company.objects.create(name='Id Software')
        Company.objects.create(name='Industrial Light & Magic', short_name='ILM')

        filter_2 = ('last_driver__employed_by', )
        self.assertEqual(generic.get_filter(Car, current_filters, filter_2), (
            u'employed by', [
                ('brand=Saab', u'All', True),
                ('brand=Saab&last_driver__employed_by__exact=1', u'Thomson Reuters', False),
                ('brand=Saab&last_driver__employed_by__exact=2', u'Id Software', False),
                ('brand=Saab&last_driver__employed_by__exact=3', u'ILM', False)
            ]
        ))

        # Set the title
        filter_3 = ('last_driver__employed_by', {'title': 'Company'})
        self.assertEqual(generic.get_filter(Car, current_filters, filter_3), (
            u'Company', [
                ('brand=Saab', u'All', True),
                ('brand=Saab&last_driver__employed_by__exact=1', u'Thomson Reuters', False),
                ('brand=Saab&last_driver__employed_by__exact=2', u'Id Software', False),
                ('brand=Saab&last_driver__employed_by__exact=3', u'ILM', False)
            ]
        ))

    def test_get_filter_through_related(self):
        current_filters = {'owner': 'Luigi'}

        Company.objects.create(name='Thomson Reuters')
        Company.objects.create(name='Id Software')
        Company.objects.create(name='Industrial Light & Magic', short_name='ILM')

        filter_1 = ('car__last_driver__employed_by', )
        self.assertEqual(generic.get_filter(Garage, current_filters, filter_1), (
            u'employed by', [
                ('owner=Luigi', u'All', True),
                ('car__last_driver__employed_by__exact=1&owner=Luigi', u'Thomson Reuters', False),
                ('car__last_driver__employed_by__exact=2&owner=Luigi', u'Id Software', False),
                ('car__last_driver__employed_by__exact=3&owner=Luigi', u'ILM', False)
            ]
        ))

        # Set the title
        filter_1 = ('car__last_driver__employed_by', {'title': 'Partners'})
        self.assertEqual(generic.get_filter(Garage, current_filters, filter_1), (
            u'Partners', [
                ('owner=Luigi', u'All', True),
                ('car__last_driver__employed_by__exact=1&owner=Luigi', u'Thomson Reuters', False),
                ('car__last_driver__employed_by__exact=2&owner=Luigi', u'Id Software', False),
                ('car__last_driver__employed_by__exact=3&owner=Luigi', u'ILM', False)
            ]
        ))



class GenericChangeResponseTest(TestCase):
    url_continue = '/cars/1/'
    url_add_another = '/cars/add/'
    url_default = '/cars/'

    def setUp(self):
        self.rf = RequestFactory()

    def test_generic_change_response(self):
        request = self.rf.post('/cars/1/')
        response = generic.generic_change_response(request, self.url_continue,
                                                   self.url_add_another, self.url_default)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url_default)

    def test_generic_change_response_continue(self):
        request = self.rf.post('/cars/1/', {'_continue': '1'})
        response = generic.generic_change_response(request, self.url_continue,
                                                   self.url_add_another, self.url_default)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url_continue)

    def test_generic_change_response_add_another(self):
        request = self.rf.post('/cars/1/', {'_addanother': '1'})
        response = generic.generic_change_response(request, self.url_continue,
                                                   self.url_add_another, self.url_default)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.url_add_another)


class GenericListTest(BaseGenericListTest):
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


class GenericListFiltersTest(BaseGenericListTest):
    template = 'generic_list_filters_test.html'

    @classmethod
    def setUpTestData(cls):
        super(GenericListFiltersTest, cls).setUpTestData()
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
                <li><a href="?last_driver__isnull=True">Aucun</a></li>
              </ul>
            </div>""" % (self.p1.pk, self.p2.pk)
        )
