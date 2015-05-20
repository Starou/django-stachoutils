# -*- coding: utf-8 -*-

from django import VERSION as DJ_VERSION
from django.contrib import admin, messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.http import urlencode, urlunquote
from django.utils.translation import ugettext as _
from django_stachoutils.options import paginate
from django_stachoutils.views.actions import regroup_actions

ORDER_BY_ATTR = 'o'
ORDER_TYPE_ATTR = 'ot'


def generic_change_response(request, url_continue, url_add_another, url_default):
    if "_continue" in request.POST:
        return HttpResponseRedirect(url_continue)
    elif "_addanother" in request.POST:
        return HttpResponseRedirect(url_add_another)
    else:
        return HttpResponseRedirect(url_default)


def generic_list(request, queryset, columns, template, Model, ClassAdmin=None,
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
    list_id = Model._meta.verbose_name

    # Actions.
    actions = regroup_actions(actions)
    actions_par_groupe = []
    if ClassAdmin and actions:
        adm = ClassAdmin(Model, admin.site)
        # {'invalider': (<unbound method ProgrammeAdmin.invalider>,
        #  'invalider', u'Invalider en...'), ...}
        admin_actions = adm.get_actions(request)
        for group, actions_in_group in actions:
            actions_dispos = [
                (callable(action) and action.func_name or action,
                 action in admin_actions and admin_actions[action][2] or action.short_description)
                for action in actions_in_group if action in admin_actions or callable(action)
            ]
            if actions_dispos:
                actions_par_groupe.append((group, actions_dispos))

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
        return render_to_response(template, c, context_instance=RequestContext(request))

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
    order_by, ordering = request.GET.get(ORDER_BY_ATTR, None), None
    if order_by:
        column = columns[int(order_by)]
        order_fields = column.get('order_fields', (column.get('field'), ))
        order_type = ''
        if request.GET[ORDER_TYPE_ATTR] == 'desc':
            order_type = '-'
        ordering = ['%s%s' % (order_type, order_field) for order_field in order_fields]
    elif default_order:
        ordering = default_order
    if ordering:
        queryset = queryset.order_by(*ordering)
    # Apply filters.
    current_filters = get_current_filter(request, filters, Model)
    queryset = queryset.filter(**filters_for_queryset(current_filters)).distinct()
    if qset_modifier:
        queryset = qset_modifier(queryset, *qset_modifier_args)

    count_across = queryset.count()
    page = paginate(request, queryset, paginate_by_default)

    # Filters.
    filters = [get_filter(Model, current_filters, f) for f in filters]

    # Exec action.
    if request.method == 'POST':
        action = request.POST.get('action')
        selected = request.POST.getlist('_selected_action')
        url_from = request.path + "?%s" % request.GET.urlencode()
        if not action:
            messages.add_message(request, messages.WARNING, "Veuillez sélectionner une action")
        if not selected:
            messages.add_message(request, messages.WARNING, "Veuillez sélectionner un ou plusieurs élements")
        if not action or not selected:
            return HttpResponseRedirect(url_from)

        # l'action est un callable.
        for group, actions_in_group in actions:
            for act in actions_in_group:
                if callable(act) and act.func_name == action:
                    # On filtre les objets selectionnés si le queryset est un vrai queryset.
                    if not int(request.POST.get('select_across', 0)) and hasattr(queryset, 'filter'):
                        selected = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
                        queryset = queryset.filter(pk__in=selected)
                    response = act(None, request, queryset)
                    # response is actually a ResponseLike instance: TODO
                    if response:
                        return response
                    else:
                        return HttpResponseRedirect(url_from)

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
    return render_to_response(template, c, context_instance=RequestContext(request))


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


def get_filter(model, current_filters, filtr):
    p = {
        'choices': None,
        'empty_choice': False,
        'attr':  filtr,
        'filter_test':  'exact',
    }

    if filtr.__class__.__name__ == 'tuple':
        p['attr'] = filtr[0]
        p.update(filtr[1])

    choices, empty_choice = p['choices'], p['empty_choice']
    attr, filter_test = p['attr'], p['filter_test']

    filter_string = attr
    attrs = attr.split('__')
    rel_models = attrs[:-1]
    attr = attrs[-1]
    mod = model
    for rel_model in rel_models:
        try:
            mod = mod._meta.get_field(rel_model).rel.to
        except:
            if DJ_VERSION >= (1, 8):
                mod = getattr(mod, '%s_set' % rel_model).related.related_model
            else:
                mod = getattr(mod, '%s_set' % rel_model).related.model

    field = mod._meta.get_field(attr)
    name = field.verbose_name

    if getattr(field, 'rel'):
        choices = choices or field.rel.to.objects.all()
        F = Filter
    elif field.__class__.__name__ == 'BooleanField':
        choices = (
            {'label': 'Oui', 'value': '1'},
            {'label': 'Non', 'value': '0'},
        )
        F = FilterSimple

    choices = [
        (lambda f=F(o, attr, filter_string, filter_test, current_filters): (
            f.url, f.label, f.is_selected))()
        for o in choices
    ]
    choices.insert(0, (lambda f=FilterAll(attr, filter_string, filter_test, current_filters): (
        f.url, f.label, f.is_selected))())
    if empty_choice:
        choices.append((lambda f=FilterNone(model, attr, filter_string, current_filters): (
            f.url, f.label, f.is_selected))())
    return (name, choices)


def get_current_filter(request, declared_filters, model,
                       ignore=['page', 'paginates_by', 'q', ORDER_BY_ATTR, ORDER_TYPE_ATTR]):
    flat_declared_filters = [(hasattr(f, 'encode') and f or f[0]) for f in declared_filters]
    out = {}
    for k, v in request.GET.items():
        if k.replace('__exact', '') in flat_declared_filters or is_a_filter(model, k):
            out[str(k)] = str(urlunquote(v))
    return out


def filters_for_queryset(filters):
    out = filters.copy()
    for k, v in filters.items():
        if k[-4:] == '__in':
            out[str(k)] = v.split(',')
    return out

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
            self.label = instance.__unicode__()
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
            for k, v in filters.iteritems():
                if not v:
                    del out[k]  # supp les filtres vides.
            self._url = urlencode(out)
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
        self.label = choice['label']
        self.value = choice['value']


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
    def __init__(self, model, attr, filter_string, current_filters):
        super(FilterNone, self).__init__(None, attr, filter_string, 'isnull', current_filters)
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
        return filters
