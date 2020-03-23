# -*- coding: utf-8 -*-

from past.builtins import basestring

from django.conf import settings
from django.template import Library, Context, Template
from django.utils.safestring import mark_safe
from django.utils.http import urlencode
from django.utils.translation import gettext as _

from django_stachoutils import urldecode
from django_stachoutils.views.generic import ORDER_BY_ATTR, ORDER_TYPE_ATTR


DOT = '.'
# TODO: mettre ca dans les settings.
PAGE_VAR = 'page'
PAGINATE_BY_VAR = 'paginate_by'
register = Library()


def paginator_number(page, i, get_params={}):
    if i == DOT:
        return u'... '
    elif i == page.number - 1:
        return mark_safe(u'<span class="this-page">%d</span> ' % (i + 1))
    else:
        params = get_params.copy()
        params.update({PAGE_VAR: i + 1})
        return mark_safe(u'<a href="?%s"%s>%d</a> ' % (urlencode(params), (i == page.paginator.num_pages - 1 and ' class="end"' or ''), i + 1))
paginator_number = register.simple_tag(paginator_number)


def paginate_by_number(page, i, current_pagination, get_params={}):
    if i == DOT:
        return u'... '
    elif i == current_pagination:
        return mark_safe(u'<span class="this-page">%s</span> ' % str(i))
    else:
        params = get_params.copy()
        params.update({PAGINATE_BY_VAR: i})
        params = sorted([(k, v) for k, v in params.items()])
        return mark_safe(u'<a href="?%s"%s>%s</a> ' % (urlencode(params), '', str(i)))
paginate_by_number = register.simple_tag(paginate_by_number)


# Librement inspiré de : http://code.djangoproject.com/browser/django/trunk/django/contrib/admin/templatetags/admin_list.py
def pagination(page, current_pagination, paginates_by=[], get_params={}):
    paginates_by = paginates_by and (paginates_by + ['All']) or []
    paginator = page.paginator
    pagination_required = (paginator.num_pages - 1)
    if not pagination_required:
        page_range = []
    else:
        ON_EACH_SIDE = 3
        ON_ENDS = 2

        if paginator.num_pages <= 10:
            page_range = range(paginator.num_pages)
        else:
            page_range = []
            if page.number > (ON_EACH_SIDE + ON_ENDS):
                page_range.extend(range(0, ON_EACH_SIDE - 1))
                page_range.append(DOT)
                page_range.extend(range(page.number - ON_EACH_SIDE, page.number + 1))
            else:
                page_range.extend(range(0, page.number + 1))
            if page.number < (paginator.num_pages - ON_EACH_SIDE - ON_ENDS - 1):
                page_range.extend(range(page.number + 1, page.number + ON_EACH_SIDE + 1))
                page_range.append(DOT)
                page_range.extend(range(paginator.num_pages - ON_ENDS, paginator.num_pages))
            else:
                page_range.extend(range(page.number + 1, paginator.num_pages))

    return {
        'page': page,
        'pagination_required': pagination_required,
        'paginates_by_required': paginates_by and True or False,
        'page_range': page_range,
        'nb_resultats': page.paginator.count,
        'paginates_by': paginates_by,
        'get_params': get_params,
        'current_pagination': current_pagination,
    }
pagination = register.inclusion_tag('django_stachoutils/pagination.html')(pagination)


@register.filter
def iconify(value):
    """Transforme un boolean en image."""
    return mark_safe("<img src='%sdjango_stachoutils/img/icon-%s.gif' />" % (
        settings.STATIC_URL, value and 'yes' or 'no'))


@register.filter
def processing(value):
    """Show a kind of alert if True."""
    return mark_safe("<img src='%sdjango_stachoutils/img/%s' />" % (
        settings.STATIC_URL, value and 'processing.png' or 'icon-yes.gif'))


@register.filter
def default_if_newrecord(record, default):
    if record.pk:
        return record
    else:
        return default


@register.filter
def truncate(value, arg):
    """ http://djangosnippets.org/snippets/163/ """
    try:
        length = int(arg)
    except ValueError:
        return value
    if not isinstance(value, basestring):
        value = str(value)
    if (len(value) > length):
        return value[:length] + "..."
    else:
        return value


@register.filter
def mod(value, arg):
    return value % arg


@register.filter
def progressbar(value):
    if isinstance(value, tuple):
        progress = value[0]
        total = value[1]
        perc_completed = 0
        if total > 0:
            perc_completed = progress / total * 100  # FIXME with Integers.
            label = "%s/%s" % (progress, total)
    else:
        perc_completed = int(value)
        label = perc_completed

    color = '#009ACD'
    if perc_completed == 100:
        color = '#BCEE68'

    return mark_safe("""
        <div class="meter-wrap">
            <div class="meter-value" style="background-color: %s; width: %s%%;">
                <div class="meter-text">
                    %s
                </div>
            </div>
        </div>""" % (color, perc_completed, label))


DOWN_STYLE = 'down'
UP_STYLE = 'up'


@register.filter
def trend_class(value):
    if value < 0:
        return DOWN_STYLE
    elif value > 0:
        return UP_STYLE


@register.filter
def current_filters(filters):
    """HTML render of the active filters from a generic_list. """
    # Selected filter, except 'All'.
    out = [(f[0], [choice[1] for choice in f[1] if choice[2]]) for f in filters]
    return [mark_safe(u'%s: <strong>%s</strong>' % (k, v[0]))
            for k, v in out if (v and v[0] != _("All"))]


# Générateur des lignes de tableaux d'index génériques.


@register.simple_tag
def table_header_tag(columns, current_url):
    out = ['<th class="action-checkbox-column"> <input id="action-toggle" type="checkbox" style="display: inline;"></th>']
    get_params = urldecode(current_url)
    out += _table_header(columns, get_params)
    return mark_safe(u' '.join(out))


def _table_header(columns, get_params, padding=0, sortable=True):
    out = []
    for i, c in enumerate(columns):
        _get_params = get_params.copy()
        if 'with' in c:
            out += _table_header(c['columns'], _get_params, i, False)
        if 'label' in c:
            style = []
            link = u'%s' % c['label']
            if sortable:
                order_type = 'asc'
                order_by = get_params.get(ORDER_BY_ATTR)
                if order_by and order_by == str(i + padding):
                    style.append('sorted')
                    if get_params[ORDER_TYPE_ATTR] == 'asc':
                        style.append('ascending')
                        order_type = 'desc'
                    else:
                        style.append('descending')
                _get_params.update({ORDER_BY_ATTR: i + padding, ORDER_TYPE_ATTR: order_type})
                _get_params = sorted([(k, v) for k, v in _get_params.items()])
                link = u'<a href="?%s">%s</a>' % (urlencode(_get_params), link)
            out.append(u'<th%s>%s<input class="fieldname" type="hidden" value="%s"/></th>' % (
                (style and ' class="%s"' % ' '.join(style) or ''), link, c['field']
            ))
    return out


@register.simple_tag
def table_row_tag(columns, instance):
    out = ['<td class="pk"><input type="checkbox" name="_selected_action" value="%d" class="action-select"></td>' % instance.pk]
    out += _table_row(columns, instance)
    return mark_safe(u' '.join(out))


def _table_row(columns, instance):
    out = []
    for c in columns:
        if 'with' in c:
            out += _table_row(c['columns'], getattr(instance, c['with'])())
        else:
            style = []
            if 'label' in c:
                value = instance
                # related lookup. On utilise pas qset.values() en amont qui eviterait ce truc récursif
                # car empêche d'accéder des attr virtuels sur les instances.
                for attr in c['field'].split('__'):
                    if value:
                        if hasattr(value, 'items'):
                            value = value.get(attr)
                        else:
                            value = getattr(value, attr)
                            if callable(value):
                                value = value()
                    else:
                        break
                if c.get('render'):
                    params = get_render_params(instance, c.get('render_params'))
                    value = getattr(value, c['render'])(*params)
                if c.get('tags'):
                    for tag in c['tags']:
                        value = tag(value)
                if value and 'link' in c:
                    href, title, a_style = "", "", ""
                    if 'href' in c['link']:
                        href = getattr(instance, c['link']['href'])()
                    if 'title' in c['link']:
                        title = getattr(instance, c['link']['title'])()
                    if 'style' in c['link']:
                        a_style = ' class="%s"' % c["link"]["style"]
                    value = u'<a%s title="%s" href="%s">%s</a>' % (a_style, title, href, value)
                if c.get('editable'):
                    style.append('editable')
                t = (value and value or '-')
                if c.get('filters') and t != '-':
                    t = Template(u'{{ value%s }}' % get_template_filters(c['filters'])).render(Context({'value': t}))
                out.append(u'<td class="%s">%s</td>' % (u' '.join(style), t))
    return out


def get_render_params(instance, params):
    out = []
    if params:
        out = list(params)
        try:
            out[out.index('self')] = instance
        except ValueError:
            pass
    return out


def get_template_filters(filters):
    t = []
    for f in filters:
        if len(f) < 2:
            t.append(u'|%s' % f[0])
        else:
            t.append(u'|%s:"%s"' % (f[0], f[1]))
    return u''.join(t)


## Inline-extras ##


def inline_visible(inlines_visibles, inline_name, current_instance_number):
    visible = True
    current_instance_number = str(current_instance_number)
    if inline_name in inlines_visibles:
        visible = False
        visibles = inlines_visibles[inline_name].split(",")
        if current_instance_number in visibles:
            visible = True
    return visible


@register.simple_tag
def inline_display_class(inlines_visibles, inline_name, current_instance_number):
    out = ""
    if not inline_visible(inlines_visibles, inline_name, current_instance_number):
        out = "closed"
    return mark_safe(out)


@register.simple_tag
def inline_display_style(inlines_visibles, inline_name, current_instance_number):
    out = ""
    if not inline_visible(inlines_visibles, inline_name, current_instance_number):
        out = "display: none;"
    return mark_safe(out)
