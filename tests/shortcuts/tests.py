# -*- coding: utf-8 -*-

import datetime
import decimal
import json
import os
import zipfile

from io import BytesIO
from django.conf import settings
from django.test import TestCase
from django_stachoutils import shortcuts


class ResponseTestCase(TestCase):
    def test_macroman_response(self):
        data = u"B#Ω"
        response = shortcuts.macroman_text_response(data)
        self.assertEqual(response.content, b'B\xf0#\xbd')

    def test_xml_response(self):
        data = u"""<?xml version="1.0"?><foo>This is a XML Document</foo>"""
        response = shortcuts.xml_response(data, filename="foo.xml")
        self.assertEqual(response.get('content-type'), 'application/xml')
        self.assertEqual(response.get('content-disposition'), 'attachment; filename="foo.xml"')

    def test_zip_response(self):
        files = [
            ("jardin.jpg", open(os.path.join(settings.MEDIA_ROOT, "jardin.jpg"), "rb").read()),
            ("terrasse.jpg", open(os.path.join(settings.MEDIA_ROOT, "terrasse.jpg"), "rb").read()),
        ]
        response = shortcuts.zip_response(files, filename='my_archive.zip')
        fp = BytesIO()
        fp.write(response.content)
        archive = zipfile.ZipFile(fp, mode='r')
        self.assertEqual(archive.namelist(), ['jardin.jpg', 'terrasse.jpg'])


class ResponseExtrasTestCase(TestCase):
    def test_encode_default(self):
        self.assertJSONEqual(json.dumps({"date": datetime.date(2018, 3, 14),
                                     "price": decimal.Decimal("14.99")},
                                    default=shortcuts.encode_default),
                         '{"date": "2018-03-14", "price": 14.99}')
