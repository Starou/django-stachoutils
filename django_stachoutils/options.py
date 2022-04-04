# -*- coding: utf-8 -*-

from django.contrib.contenttypes.models import ContentType
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.encoding import force_str

from django.core.paginator import Paginator, InvalidPage, EmptyPage


def log_addition(request_or_user, obj, message="Creation"):
    if hasattr(request_or_user, 'user'):
        user_id = request_or_user.user.pk
    else:
        user_id = request_or_user.pk
    LogEntry.objects.log_action(
        user_id         = user_id,
        content_type_id = ContentType.objects.get_for_model(obj).pk,
        object_id       = obj.pk,
        object_repr     = force_str(obj),
        action_flag     = ADDITION,
        change_message  = message
    )


def log_change(request_or_user, obj, message):
    if hasattr(request_or_user, 'user'):
        user_id = request_or_user.user.pk
    else:
        user_id = request_or_user.pk
    LogEntry.objects.log_action(
        user_id         = user_id,
        content_type_id = ContentType.objects.get_for_model(obj).pk,
        object_id       = obj.pk,
        object_repr     = force_str(obj),
        action_flag     = CHANGE,
        change_message  = message
    )


def log_deletion(request_or_user, obj, object_repr):
    if hasattr(request_or_user, 'user'):
        user_id = request_or_user.user.pk
    else:
        user_id = request_or_user.pk
    LogEntry.objects.log_action(
        user_id         = user_id,
        content_type_id = ContentType.objects.get_for_model(obj).pk,
        object_id       = obj.pk,
        object_repr     = object_repr,
        action_flag     = DELETION
    )


def log_change_for_user(user, obj, message):
    LogEntry.objects.log_action(
        user_id         = user.pk,
        content_type_id = ContentType.objects.get_for_model(obj).pk,
        object_id       = obj.pk,
        object_repr     = force_str(obj),
        action_flag     = CHANGE,
        change_message  = message
    )


def logs_for_formsets(mode, request_or_user, obj, forms):
    """forms est une liste de forms ou formsets."""
    if mode == 'addition':
        log_addition(request_or_user, obj)
    elif mode == 'change':
        msg = u'a modifié : '
        for f in forms:
            msg += _log_for_forms(f)
        log_change(request_or_user, obj, msg)


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
    elif 'paginate_by' in request.GET:
        try:
            paginate_by = int(request.GET['paginate_by'])
        except ValueError:
            pass  # on retombe sur la valeur par defaut.

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
