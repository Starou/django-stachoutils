from distutils.core import setup
import os
import sys

setup(
    name="Adencf Commons",
    version="1.0",
    author='Stanislas Guerra',
    author_email='stan@slashdev.me',
    description='',
    long_description = '',
    packages=[
        'adencf_commons', 
        'adencf_commons.management', 
        'adencf_commons.management.commands', 
        'adencf_commons.forms', 
        'adencf_commons.views', 
        'adencf_commons.templatetags', 
        'adencf_commons.tests', 
    ],
    package_data={
        'adencf_commons': [
            'static/adencf_commons/css/*.css',
            'static/adencf_commons/js/*.js',
            'static/adencf_commons/img/*.png',
            'static/adencf_commons/img/*.jpg',
            'static/adencf_commons/img/*.gif',
            'templates/adencf_commons/*.html',
        ]
    },
    data_files=[],
    scripts = [],
)
