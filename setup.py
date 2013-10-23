from distutils.core import setup
import os
import sys

setup(
    name="Stachou Utils",
    version="0.90",
    author='Stanislas Guerra',
    author_email='stan@slashdev.me',
    description='Commons for Django',
    long_description = '',
    packages=[
        'django_stachoutils', 
        'django_stachoutils.management', 
        'django_stachoutils.management.commands', 
        'django_stachoutils.forms', 
        'django_stachoutils.views', 
        'django_stachoutils.templatetags', 
        'django_stachoutils.tests', 
    ],
    package_data={
        'django_stachoutils': [
            'static/django_stachoutils/css/*.css',
            'static/django_stachoutils/js/*.js',
            'static/django_stachoutils/img/*.png',
            'static/django_stachoutils/img/*.jpg',
            'static/django_stachoutils/img/*.gif',
            'templates/django_stachoutils/*.html',
        ]
    },
    data_files=[],
    scripts = [],
)
