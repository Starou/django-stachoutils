# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.translation import ugettext as _
from django.utils.encoding import force_unicode
from django.utils.text import capfirst
from django.utils.http import urlencode

from django.core.paginator import Paginator, InvalidPage, EmptyPage

def detail_historique(request, model, object_id):
    opts = model._meta
    app_label = opts.app_label
    action_list = LogEntry.objects.filter(
        object_id = object_id,
        content_type__id__exact = ContentType.objects.get_for_model(model).id
    ).select_related().order_by('action_time')
    obj = get_object_or_404(model, pk=object_id)
    context = {
        'title': _('Change history: %s') % force_unicode(obj),
        'action_list': action_list,
        'module_name': capfirst(force_unicode(opts.verbose_name_plural)),
        'object': obj,
        'root_path': '',
        'app_label': app_label,
    }
    context_instance = RequestContext(request)
    return render_to_response([
        "admin/%s/%s/object_history.html" % (app_label, opts.object_name.lower()),
        "admin/%s/object_history.html" % app_label,
        "admin/object_history.html"
    ], context, context_instance=context_instance)


def log_addition(request, object):
    LogEntry.objects.log_action(
        user_id         = request.user.pk,
        content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id       = object.pk,
        object_repr     = force_unicode(object),
        action_flag     = ADDITION
    )


def log_change(request, object, message):
    LogEntry.objects.log_action(
        user_id         = request.user.pk,
        content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id       = object.pk,
        object_repr     = force_unicode(object),
        action_flag     = CHANGE,
        change_message  = message
    )


def log_deletion(request, object, object_repr):
    LogEntry.objects.log_action(
        user_id         = request.user.id,
        content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id       = object.pk,
        object_repr     = object_repr,
        action_flag     = DELETION
    )


def log_change_for_user(user, object, message):
    LogEntry.objects.log_action(
        user_id         = user.pk,
        content_type_id = ContentType.objects.get_for_model(object).pk,
        object_id       = object.pk,
        object_repr     = force_unicode(object),
        action_flag     = CHANGE,
        change_message  = message
    )


def logs_for_formsets(mode, request, object, forms):
    """forms est une liste de forms ou formsets."""
    if mode == 'addition':
        log_addition(request, object)
    elif mode == 'change':
        msg = u'a modifié : '
        for f in forms:
            msg += _log_for_forms(f)
        log_change(request, object, msg)


def _log_for_forms(f):
    msg = ''
    if hasattr(f, 'changed_data'):
        if f.changed_data:
            msg += u', '.join(f.changed_data)
            if hasattr(f, 'instance'):
                msg += u' (%s [%s]) ; ' % (f.instance._meta.verbose_name, f.instance)
            else:
                msg += u' (%s) ; ' % (f.__class__.__name__)
    if hasattr(f, 'forms'):
        for f2 in f.forms:
            msg += _log_for_forms(f2)
    return msg



def paginate(request, queryset, paginate_by=50):
    if request.GET.get('paginate_by') == 'All':
        paginate_by = queryset.count()
    elif request.GET.has_key('paginate_by'):
        try:
            paginate_by = int(request.GET['paginate_by'])
        except ValueError:
            pass # on retombe sur la valeur par defaut.

    paginator = Paginator(queryset, paginate_by)
    try:
        num_page = int(request.GET.get('page', '1'))
    except ValueError:
        num_page = 1
    try:
        page = paginator.page(num_page)
    except (EmptyPage, InvalidPage):
        page = paginator.page(paginator.num_pages)

    return page
