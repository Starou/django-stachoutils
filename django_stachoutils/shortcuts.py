import csv
import decimal
import datetime
import sys
import zipfile

from cStringIO import StringIO
from django.http import HttpResponse
from django.shortcuts import _get_queryset
from django_stachoutils import csv_utf8


def macroman_text_response(data, filename=None, encode=True):
    if encode:
        data = data.encode('macroman')
    response = HttpResponse(data, content_type="text/plain; charset=macintosh")
    if filename:
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response


def encode_default(d):
    if isinstance(d, decimal.Decimal):
        return float(str(d))
    elif isinstance(d, datetime.date) or isinstance(d, datetime.datetime):
        return d.isoformat()
    raise TypeError


def get_object_or_none(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def xml_response(data, filename=None):
    response = HttpResponse(data, content_type='application/xml')
    if filename:
        response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    return response


def zip_response(files, filename):
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'filename=%s' % filename

    buffer = StringIO()
    zip = zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED)
    for name, f in files:
        if sys.version_info < (2, 6):
            name = name.encode('latin1')
        zip.writestr(name, f)
    zip.close()
    buffer.flush()
    ret_zip = buffer.getvalue()
    buffer.close()
    response.write(ret_zip)
    return response


def csv_response(rows, filename, kwargs={'delimiter': ',', 'quoting': csv.QUOTE_ALL}):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    writer = csv_utf8.UnicodeWriter(response, **kwargs)
    writer.writerows(rows)
    return response


def createAndAppendElement(document, parentNode, tagName, text=None):
    node = document.createElement(tagName)
    parentNode.appendChild(node)
    if text:
        node.appendChild(document.createTextNode(text))
    return node
