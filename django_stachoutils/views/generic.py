# -*- coding: utf-8 -*-

from builtins import object
from builtins import str as text
from django.contrib import admin, messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.contrib.admin.utils import label_for_field
from django.db.models import Q
from django.db.models.query import QuerySet
from django.db.models.fields import BooleanField
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import urlencode, urlunquote
from django.utils.translation import gettext as _
from django_stachoutils.options import paginate
from django_stachoutils.views.actions import regroup_actions

ORDER_BY_ATTR = 'o'
ORDER_TYPE_ATTR = 'ot'

FILTER_IGNORE_DEFAULT = ['page', 'paginates_by', 'q', ORDER_BY_ATTR, ORDER_TYPE_ATTR]


def generic_change_response(request, url_continue, url_add_another, url_default):
    if "_continue" in request.POST:
        return HttpResponseRedirect(url_continue)
    elif "_addanother" in request.POST:
        return HttpResponseRedirect(url_add_another)
    else:
        return HttpResponseRedirect(url_default)


def generic_list(request, queryset, columns, template, model, ClassAdmin=None,
                 actions=[], filters=(), links=(), search=(), default_order=None,
                 paginate_by_default=100, paginates_by=[], qset_modifier=None,
                 qset_modifier_args=[], extra_params={}):
    """
     actions_par_groupe = [
        ('groupeA', [('action_1', 'libellé de l'action 1'),
                     ('action_3', 'libellé de l'action 3')]),
        ('groupeB', [('action_2', 'libellé de l'action 2')]),
     ]
    """
    list_id = model._meta.verbose_name
    set_columns_labels(model, columns)

    # Actions.
    actions = regroup_actions(actions)
    actions_par_groupe = []
    if ClassAdmin and actions:
        adm = ClassAdmin(model, admin.site)
        # {'invalider': (<unbound method ProgrammeAdmin.invalider>,
        #  'invalider', u'Invalider en...'), ...}
        admin_actions = adm.get_actions(request)
        for group, actions_in_group in actions:
            actions_dispos = [
                (callable(action) and action.__name__ or action,
                 action in admin_actions and admin_actions[action][2] or action.short_description)
                for action in actions_in_group if action in admin_actions or callable(action)
            ]
            if actions_dispos:
                actions_par_groupe.append((group, actions_dispos))

    # Exec action.
    if request.method == 'POST':
        action = request.POST.get('action')
        selected = request.POST.getlist('_selected_action')
        url_from = request.path + "?%s" % request.GET.urlencode()
        if not action:
            messages.add_message(request, messages.WARNING, "Veuillez sélectionner une action")
        if not selected:
            messages.add_message(request, messages.WARNING,
                                 "Veuillez sélectionner un ou plusieurs élements")
        if not action or not selected:
            return HttpResponseRedirect(url_from)

        # l'action est un callable.
        for group, actions_in_group in actions:
            for act in actions_in_group:
                if callable(act) and act.__name__ == action:
                    # On filtre les objets selectionnés si le queryset est un vrai queryset.
                    if not int(request.POST.get('select_across', 0)) and hasattr(queryset, 'filter'):
                        selected = request.POST.getlist(ACTION_CHECKBOX_NAME)
                        queryset = queryset.filter(pk__in=selected)
                    response = act(None, request, queryset)
                    # response is actually a ResponseLike instance: TODO
                    if response:
                        return response
                    else:
                        return HttpResponseRedirect(url_from)

    # Si le queryset est une liste, on skip pas mal de choses.
    if not hasattr(queryset, 'filter'):
        c = {
            'object_list': queryset,
            'page': None,
            'get_params': dict(request.GET.items()),
            'actions': actions_par_groupe,
            'links': links,
            'path': request.path,
            'full_path': u'%s?%s' % (request.path, request.GET.urlencode()),
            'list_id': list_id,
        }
        c.update(extra_params)
        return render(request, template, c)

    # Filter columns according to the user permissions.
    columns = [col for col in columns if has_column_perm(request.user, col)]

    # Search.
    if request.GET.get('q'):
        query = request.GET['q']
        q_filters = [Q(**{s[1]: query}) for s in search]
        f = q_filters.pop()
        for filt in q_filters:
            f = f | filt
        queryset = queryset.filter(f)

    # Queryset.
    ordering = get_ordering_params(request, model, columns, default_order)
    if ordering:
        queryset = queryset.order_by(*ordering)

    # Apply filters.
    current_filters = get_current_filters(request, filters, model)
    queryset = filter_queryset(queryset, filters, current_filters, qset_modifier,
                               qset_modifier_args)
    count_across = queryset.count()
    page = paginate(request, queryset, paginate_by_default)

    # Filters.
    filters = [get_filter(model, current_filters, f) for f in filters]

    c = {
        'object_list': page.object_list,
        'page': page,
        'paginate_by': request.GET.get('paginate_by', paginate_by_default),
        'paginates_by': request.GET.get('paginates_by', paginates_by),
        'columns': columns,
        'actions': actions_par_groupe,
        'filters': filters,
        'links': links,
        'search': [s[0] for s in search],
        'get_params': dict(request.GET.items()),
        'path': request.path,
        'full_path': u'%s?%s' % (request.path, request.GET.urlencode()),
        'list_id': list_id,
        'count_across': count_across,
    }
    c.update(extra_params)
    return render(request, template, c)


def set_columns_labels(model, columns):
    for col in columns:
        if 'columns' in col:
            set_columns_labels(model, col['columns'])
        elif 'label' not in col:
            col['label'] = label_for_field(col['field'], model)


def get_ordering_params(request, model, columns, default_order):
    order_by, ordering = request.GET.get(ORDER_BY_ATTR, None), None

    if order_by:
        column = columns[int(order_by)]

        if 'ordering' in column:
            order_fields = column.get('ordering')
        else:
            attr_name = column['field']
            try:
                attr = getattr(model, attr_name)
            # Some fields are not reachable but we don't care,
            # we are looking for a method here.
            except AttributeError:
                attr = None
            if hasattr(attr, 'ordering'):
                order_fields = attr.ordering
            else:
                order_fields = [attr_name]

        order_type = ''
        if request.GET[ORDER_TYPE_ATTR] == 'desc':
            order_type = '-'

        ordering = ['%s%s' % (order_type, order_field) for order_field in order_fields]

    elif default_order:
        ordering = default_order

    return ordering


def has_column_perm(user, column):
    perms = column.get('perms')
    if not perms:
        return True
    for perm in perms:
        if perm[0] == '!':
            user_has_perm = not user.has_perm(perm[1:])
        else:
            user_has_perm = user.has_perm(perm)
        if not user_has_perm:
            return False
    return True


def filter_queryset(queryset, filters, current_filters, modifier, modifier_args):
    filter_attrs = {}
    filters_as_dict = dict([(f[0], f[1] if len(f) == 2 else {}) for f in filters])
    for key, value in current_filters.items():
        root_key = key.replace('__exact', '')
        filter_params = filters_as_dict.get(root_key)
        # filter can provide its own custom queryset filtering
        # or just be a parameter to the main filtering call.
        try:
            queryset = filter_params['queryset'](queryset, value)
        except (KeyError, TypeError):
            filter_attrs[key] = value

    queryset = queryset.filter(**filters_for_queryset(filter_attrs)).distinct()
    if modifier:
        queryset = modifier(queryset, *modifier_args)
    return queryset


def filters_for_queryset(current_filters):
    qset_filter_params = current_filters.copy()
    for k, v in current_filters.items():
        if k[-4:] == '__in':
            qset_filter_params[str(k)] = v.split(',')
    return qset_filter_params


def get_filter(model, current_filters, filter_params):
    """
    o filter_params may be a 1 elt or a 2 elts tuple

    Return a tuple:

    "filter title",
    [
        (label, url, is_selected),  # filter value #1
        (label, url, is_selected),  # filter value #2
        ...
    ]
    """

    params = {
        'filter_key': filter_params[0],
        'title': None,
        'queryset': None,
        'choices': None,
        'empty_choice': False,
        'filter_test': 'exact',
    }
    try:
        params.update(filter_params[1])
    except IndexError:
        pass

    choices, empty_choice = params['choices'], params['empty_choice']
    filter_key, filter_test = params['filter_key'], params['filter_test']
    title = params['title']

    field, attrib = None, None

    def discover_field(model, filter_key):
        attrs = filter_key.split('__')
        rel_models = attrs[:-1]
        attr = attrs[-1]
        mod = model
        for rel_model in rel_models:
            mod = mod._meta.get_field(rel_model).remote_field.model
        field = mod._meta.get_field(attr)

        return field, attr

    if not title:
        field, attrib = discover_field(model, filter_key)
        title = field.verbose_name

    if choices:
        FilterKlass = FilterSimple
        if type(choices) == QuerySet:
            FilterKlass = Filter
    else:
        if not field:
            field, attrib = discover_field(model, filter_key)
        if type(field) == BooleanField:
            FilterKlass = FilterSimple
            choices = [
                ('1', 'Oui'),
                ('0', 'Non'),
            ]
        else:
            FilterKlass = Filter
            choices = field.remote_field.model.objects.all()

    def get_displayed_choices(FilterKlass, choices, current_filters, filter_test,
                              filter_key, model, attrib):
        displayed_choices = [
            (lambda f=FilterKlass(o, attrib, filter_key, filter_test, current_filters): (
                f.url, f.label, f.is_selected))()
            for o in choices
        ]
        displayed_choices.insert(0, (lambda f=FilterAll(attrib, filter_key, filter_test, current_filters): (
            f.url, f.label, f.is_selected))())
        if empty_choice:
            displayed_choices.append((lambda f=FilterNone(model, attrib, filter_key, filter_test, current_filters): (
                f.url, f.label, f.is_selected))())

        return displayed_choices

    displayed_choices = get_displayed_choices(FilterKlass, choices, current_filters,
                                              filter_test, filter_key, model, attrib)

    return title, displayed_choices


def get_current_filters(request, filters, model, ignore=FILTER_IGNORE_DEFAULT):
    """ Return {'key': 'value', ...} """

    filters_keys = [f[0] for f in filters]

    current_filters = {}
    for k, v in request.GET.items():
        if k.replace('__exact', '') in filters_keys or is_a_filter(model, k):
            current_filters[str(k)] = str(urlunquote(v))
    return current_filters


##

LOOKUPS = [
    'exact',
    'iexact',
    'contains',
    'icontains',
    'in',
    'gt',
    'gte',
    'lt',
    'lte',
    'startswith',
    'istartswith',
    'endswith',
    'iendswith',
    'range',
    'year',
    'month',
    'day',
    'week_day',
    'isnull',
    'search',
    'regex',
    'iregex',
]


def is_a_filter(model, filtr):
    instance = model()
    lst = filtr.split('__')
    if lst[-1] in LOOKUPS:
        del lst[-1]
    if hasattr(instance, lst[0]):
        return True


class Filter(object):
    """An object to represente the filters in the index pages. Works on FK. """

    def __init__(self, instance, attr, filter_string, test, current_filters):
        if instance:
            self.instance = instance
            self.label = text(instance)
            self.value = str(instance.pk)
        self.current_filters = current_filters
        self.key = '%s__%s' % (filter_string, test)
        self.isnull = '%s__isnull' % (filter_string,)
        self._url = None
        self._is_selected = None

    def _get_url(self):
        """L'url d'un filtre doit conserver les filtres en cours pour être additifs. """
        if self._url is None:
            filters = self.get_base_filters()
            out = filters.copy()
            for k, v in filters.items():
                if not v:
                    del out[k]  # del empty filters
            self._url = urlencode(sorted((k, v) for k, v in out.items()))  # sorted to pass the tests...
        return self._url
    url = property(_get_url)

    def get_base_filters(self):
        filters = self.current_filters.copy()
        # on update le parametre si deja present dans l'url.
        filters.update({self.key: self.value})
        # on vire l'eventuel filtre is_null.
        if self.isnull in filters:
            del filters[self.isnull]
        return filters

    def _get_is_selected(self):
        """L'url d'un filtre doit conserver les filtres en cours pour être additifs. """
        if self._is_selected is None:
            selected = self.current_filters.get(self.key, None)
            self._is_selected = (self.value == selected)
        return self._is_selected
    is_selected = property(_get_is_selected)


class FilterSimple(Filter):
    def __init__(self, choice, attr, filter_string, test, current_filters):
        super(FilterSimple, self).__init__(None, attr, filter_string, test, current_filters)
        self.label = choice[1]
        self.value = str(choice[0])


class FilterAll(Filter):
    """Désactive le filtre en selectionnant tous les objects. """

    def __init__(self, attr, filter_string, test, current_filters):
        super(FilterAll, self).__init__(None, attr, filter_string, test, current_filters)
        self.label = _("All")
        self.value = None

    def _get_is_selected(self):
        if self._is_selected is None:
            if self.key not in self.current_filters and self.isnull not in self.current_filters:
                self._is_selected = True
        return self._is_selected
    is_selected = property(_get_is_selected)

    def get_base_filters(self):
        """L'url est construite à partir de l'url en cours, en supp l'eventuel filtre sur le groupe. """
        filters = super(FilterAll, self).get_base_filters()
        filters.pop(self.key, None)
        return filters


class FilterNone(Filter):
    def __init__(self, model, attr, filter_string, test, current_filters):
        super(FilterNone, self).__init__(None, attr, filter_string, 'isnull', current_filters)
        self.sibling_key = '%s__%s' % (filter_string, test)  # key for actual filtering
        self.label = u'Aucun'
        self.value = True

    def _get_is_selected(self):
        if self.isnull in self.current_filters:
            self._is_selected = True
        return self._is_selected
    is_selected = property(_get_is_selected)

    def get_base_filters(self):
        filters = super(FilterNone, self).get_base_filters()
        filters.update({self.key: self.value})
        if self.sibling_key in filters:
            del filters[self.sibling_key]
        return filters
