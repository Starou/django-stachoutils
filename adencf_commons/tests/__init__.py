# -*- coding: utf-8 -*-

from django.test import TestCase
from django.test.testcases import to_list
from django.conf import settings
import tempfile
import os, shutil

from adencf_commons import lowerize, NO_CAPFIRST

class PublishTestCase(TestCase):
    def setUp(self):
        self.old_dossier_watch_dir  = settings.DOSSIERS_WATCH_DIR 
        settings.DOSSIERS_WATCH_DIR = os.path.join(tempfile.gettempdir(), 'watch')
        if os.path.exists(settings.DOSSIERS_WATCH_DIR):
            shutil.rmtree(settings.DOSSIERS_WATCH_DIR)
        os.mkdir(settings.DOSSIERS_WATCH_DIR)

    def tearDown(self):
        shutil.rmtree(settings.DOSSIERS_WATCH_DIR)
        settings.DOSSIERS_WATCH_DIR = self.old_dossier_watch_dir

    def assertFormSetError(self, response, formset, index, field, errors):
        """
        Asserts that a formset used to render the response has a specific error.
        """
        # Put context(s) into a list to simplify processing.
        contexts = to_list(response.context)
        if not contexts:
            self.fail('Response did not use any contexts to render the response')

        # Put error(s) into a list to simplify processing.
        errors = to_list(errors)

        # Search all contexts for the error.
        found_formset = False
        for i,context in enumerate(contexts):
            if formset not in context:
                continue
            found_formset = True
            for err in errors:
                if field:
                    if field in context[formset].forms[index].errors:
                        field_errors = context[formset].forms[index].errors[field]
                        self.failUnless(err in field_errors,
                                "The field '%s' on formset '%s' [%s] in"
                                " context %d does not contain the"
                                " error '%s' (actual errors: %s)" %
                                        (field, formset, index, i, err,
                                        repr(field_errors)))
                    elif field in context[formset].forms[index].fields:
                        self.fail("The field '%s' on formset '%s' [%s] in context %d"
                                  " contains no errors" % (field, form, index, i))
                    else:
                        self.fail("The formset '%s' [%s] in context %d does not"
                                  " contain the field '%s'" %
                                        (formset, index, i, field))
                elif index is not None:
                    non_field_errors = context[formset].forms[index].non_field_errors()
                    self.failUnless(err in non_field_errors,
                        "The formset '%s' [%s] in context %d does not contain the"
                        " non-field error '%s' (actual errors: %s)" %
                        (formset, index, i, err, non_field_errors))
                else:
                    print dir(context[formset])
                    non_form_errors = context[formset].non_form_errors()
                    self.failUnless(err in non_form_errors,
                        "The formset '%s' in context %d does not contain the"
                        " non-form error '%s' (actual errors: %s)" %
                        (formset, i, err, non_form_errors))
        if not found_formset:
            self.fail("The formset '%s' was not used to render the response" % formset)
    
def dict_diff(d1, d2):
    """
    >>> d1 = {'a': 12, 'b': 23}
    >>> d2 = {'a': 11, 'b': 23, 'c': 16}
    >>> dict_diff(d1, d2)
    {'a': (12, 11), 'c': (None, 16)}
    """
    diff = {}
    for key in d1.keys()+d2.keys():
        both_has_key = True
        try:
            x = d1[key]
        except KeyError:
            diff[key] = (None, d2[key])
            both_has_key = False
        try:
            x = d2[key]
        except KeyError:
            diff[key] = (d1[key], None)
            both_has_key = False
        if both_has_key and (d1[key] != d2[key]):
            diff[key] = (d1[key], d2[key])
    return diff
    

def get_obj_dict(obj, extras=('id',)):
    out = obj.__dict__.copy()
    del out['_state']
    for extra in extras:
        del out[extra]
    return out


###


class UtilsTestCase(PublishTestCase):

    def test_files_are_equal(self):
        from django.core.files.base import ContentFile
        from adencf_commons import files_are_equal
        MEDIA_ROOT = os.path.join(settings.MEDIA_ROOT, 'test')
        img_root = os.path.join(MEDIA_ROOT, 'images')

        image1 = os.path.join(img_root, 'jardin.jpg')
        image2 = os.path.join(img_root, 'terrasse.jpg')
        f1 = ContentFile(open(image1, 'rb').read())
        f2 = ContentFile(open(image2, 'rb').read())

        self.assertFalse(files_are_equal(f1, f2))

        f1bis = ContentFile(open(image1, 'rb').read())
        self.assertTrue(files_are_equal(f1, f1bis))

    def test_lowerize(self):
        for test_string, expected in [
                    ('LOWER THIS', 'Lower This'),
                    ('Les Carrés De Monthoux', 'Les Carrés de Monthoux'),
                ]:
            self.assertEqual(lowerize(test_string, NO_CAPFIRST), expected)
