# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from builtins import chr, map, range, str
import hashlib
import re
import unicodedata

from datetime import datetime
from django.utils import formats, dateformat
from django.utils.encoding import force_str
from django.utils.functional import keep_lazy_text
from django.utils.http import urlunquote


def format_datetime(value=None, date=True, time=True):
    if not date:
        format_type = 'TIME_FORMAT'
    elif not time:
        format_type = 'DATE_FORMAT'
    else:
        format_type = 'DATETIME_FORMAT'
    return dateformat.format(value or datetime.now(), formats.get_format(format_type))


def format_number(value=None, separator=','):
    if not value:
        return ''

    def split_thousands(s):
        if len(s) <= 3:
            return s
        return split_thousands(s[:-3]) + separator + s[-3:]
    return split_thousands(str(value))


# From http://stackoverflow.com/questions/517923/what-is-the-best-way-to-remove-accents-in-a-python-unicode-string
def strip_accents(txt):
    return unicodedata.normalize('NFD', str(txt)).encode('ascii', 'ignore').decode('ascii')


def latin1_safe_xml_encode(txt):
    return str(txt.encode('latin-1', 'xmlcharrefreplace'), 'latin-1')


xml_entity_table = bytes.maketrans(b' \'', b'--')


def format_xml_entity(txt):
    return strip_accents(txt).encode('ascii').upper().translate(xml_entity_table)


@keep_lazy_text
def truncate_chars(s, num):
    "Truncates a string after a certain number of characters."
    txt = force_str(s)
    length = int(num)
    if len(txt) > length:
        txt = txt[:length] + '...'
    return txt


rx_lettrine = re.compile(r"(\w)(\s)([\w-]+)([,.]{0,1}\s.*)", re.UNICODE | re.IGNORECASE)


def clean_lettrine(txt):
    """Vire les espaces ajoutés aux textes suite import QuarkXpress"""
    match = rx_lettrine.match(txt)
    if match:
        match = match.groups()
        supp_premier_espace = True
        if match[0] == 'A':
            if match[2] not in ('u', 'ux', 'vec', 'utour',):
                supp_premier_espace = False
        if supp_premier_espace:
            txt = rx_lettrine.sub(r'\1\3\4', txt)
    return txt


# From http://www.daniweb.com/code/snippet216865.html
#
# convert an integer to a roman numeral
# keep it reasonable since from 5000 on special characters are used
# see also: http://en.wikipedia.org/wiki/Roman_numerals
# tested with Python24       vegaseat        25jan2007
def int_to_roman(number):
    numerals = {1: "I", 4: "IV", 5: "V", 9: "IX", 10: "X", 40: "XL",
                50: "L", 90: "XC", 100: "C", 400: "CD", 500: "D", 900: "CM", 1000: "M"}
    result = ""
    for value, numeral in sorted(list(numerals.items()), reverse=True):
        while number >= value:
            result += numeral
            number -= value
    return result


# Inspired by http://stackoverflow.com/questions/92438/stripping-non-printable-characters-from-a-string-in-python
non_printable_re = re.compile('[%s]' % re.escape(''.join(map(chr, list(range(0, 9)) + list(range(11, 13)) + list(range(14, 32)) + list(range(127, 160))))))


def filter_non_printable(txt):
    return non_printable_re.sub('', txt)


def simple_decorator(decorator):
    def new_decorator(f):
        g = decorator(f)
        g.__name__ = f.__name__
        g.__doc__ = f.__doc__
        g.__dict__.update(f.__dict__)
        return g
    new_decorator.__name__ = decorator.__name__
    new_decorator.__doc__ = decorator.__doc__
    new_decorator.__dict__.update(decorator.__dict__)
    return new_decorator


def camelize(txt):
    return ' '.join([t.title() for t in txt.split(' ')])


def files_are_equal(f1, f2):
    if f1.size != f2.size:
        return False
    elif _digest_file(f1) != _digest_file(f2):
        return False
    return True


def _digest_file(f, chunk_size=8192):
    md5 = hashlib.md5()
    for chunk in iter(lambda: f.read(chunk_size), b""):
        md5.update(chunk)
    f.seek(0)
    return md5.digest()


def urldecode(url):
    out = {}
    get_params = (url.split('?')[1:] or [None])
    if get_params[0]:
        for param in get_params[0].split('&'):
            k, v = param.split('=')
            out[k] = urlunquote(v)
    return out
