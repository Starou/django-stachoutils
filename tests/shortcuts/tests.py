# -*- coding: utf-8 -*-

import csv
import datetime
import decimal
import json
import zipfile

from io import BytesIO
from xml.dom import minidom
from django.conf import settings
from django.test import TestCase
from django_stachoutils import shortcuts
from pathlib import Path


class ResponseTest(TestCase):
    def test_macroman_response(self):
        data = u"B#Ω"
        response = shortcuts.macroman_text_response(data)
        self.assertEqual(response.content, b'B\xf0#\xbd')

    def test_macroman_response_with_filename(self):
        data = u"B#Ω"
        response = shortcuts.macroman_text_response(data, filename='export.txt')
        self.assertEqual(response.content, b'B\xf0#\xbd')
        self.assertEqual(response['Content-Disposition'], 'attachment; filename="export.txt"')

    def test_xml_response(self):
        data = u"""<?xml version="1.0"?><foo>This is a XML Document</foo>"""
        response = shortcuts.xml_response(data, filename="foo.xml")
        self.assertEqual(response.get('content-type'), 'application/xml')
        self.assertEqual(response.get('content-disposition'), 'attachment; filename="foo.xml"')

    def test_zip_response(self):
        files = [
            ("jardin.jpg", Path(f"{settings.MEDIA_ROOT}/jardin.jpg").read_bytes()),
            ("terrasse.jpg", Path(f"{settings.MEDIA_ROOT}/terrasse.jpg").read_bytes()),
        ]
        response = shortcuts.zip_response(files, filename='my_archive.zip')
        fp = BytesIO()
        fp.write(response.content)
        archive = zipfile.ZipFile(fp, mode='r')
        self.assertEqual(archive.namelist(), ['jardin.jpg', 'terrasse.jpg'])

    def test_csv_response(self):
        rows = [
            [u"Numéro de Serie", u"Marque", u"Modèle", u"Année"],
            [u"SB2323", u"Saab", u"9.3 2.0t", u"2007"],
            [u"LDNV005", u"Lada", u"Niva", u"2009"],
        ]
        response = shortcuts.csv_response(rows, "my_data.csv",
                                          {'delimiter': '|',
                                           'quoting': csv.QUOTE_MINIMAL})
        self.assertEqual(
            response.content,
            b'Num\xc3\xa9ro de Serie|Marque|Mod\xc3\xa8le|Ann\xc3\xa9e\r\nSB2323|Saab|9.3 2.0t|2007\r\nLDNV005|Lada|Niva|2009\r\n'
        )


class ResponseExtrasTest(TestCase):
    def test_encode_default(self):
        self.assertJSONEqual(json.dumps({"date": datetime.date(2018, 3, 14),
                                         "price": decimal.Decimal("14.99")},
                                        default=shortcuts.encode_default),
                             '{"date": "2018-03-14", "price": 14.99}')

    def test_encode_default_raises_exception(self):
        from .models import Car
        self.assertRaises(TypeError, json.dumps, {
            "date": datetime.date(2018, 3, 14),
            "price": decimal.Decimal("14.99"),
            "car": Car.objects.create(brand="Saab", name="9.3"),
        }, default=shortcuts.encode_default)

    def test_get_object_or_none(self):
        from .models import Car
        c1 = Car.objects.create(brand="Subaru", name="Impreza")
        Car.objects.create(brand="Saab", name="9.3")
        self.assertIsNone(shortcuts.get_object_or_none(Car, brand="Ford", name="Mustang"))
        self.assertEqual(shortcuts.get_object_or_none(Car, brand="Subaru", name="Impreza"), c1)

    def test_create_and_append_element(self):
        impl = minidom.getDOMImplementation('')
        doc = impl.createDocument(None, 'my_elements', None)
        node = shortcuts.createAndAppendElement(doc, doc.documentElement, 'my_node')
        self.assertXMLEqual(node.toxml(), '<my_node/>')

    def test_create_and_append_element_with_text(self):
        impl = minidom.getDOMImplementation('')
        doc = impl.createDocument(None, 'my_elements', None)
        node = shortcuts.createAndAppendElement(doc, doc.documentElement, 'my_node', 'Some text')
        self.assertXMLEqual(node.toxml(), '<my_node>Some text</my_node>')
