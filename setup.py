import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as f:
    README = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name="django-stachoutils",
    version="3.3.0",
    license='BSD Licence',
    author='Stanislas Guerra',
    author_email='stan@slashdev.me',
    description='Commons for Django',
    url='https://github.com/Starou/django-stachoutils',
    project_urls={
        'Source Code': 'https://github.com/Starou/django-stachoutils',
        'Issue Tracker': 'https://github.com/Starou/django-stachoutils/issues',
    },
    long_description=README,
    install_requires=['future'],
    packages=[
        'django_stachoutils',
        'django_stachoutils.management',
        'django_stachoutils.management.commands',
        'django_stachoutils.forms',
        'django_stachoutils.views',
        'django_stachoutils.templatetags',
    ],
    package_data={
        'django_stachoutils': [
            'static/django_stachoutils/css/*.css',
            'static/django_stachoutils/js/*.js',
            'static/django_stachoutils/img/*.png',
            'static/django_stachoutils/img/*.jpg',
            'static/django_stachoutils/img/*.gif',
            'static/django_stachoutils/poshytip/*.js',
            'static/django_stachoutils/poshytip/*/*.css',
            'static/django_stachoutils/poshytip/*/*.gif',
            'static/django_stachoutils/poshytip/*/*.png',
            'templates/django_stachoutils/*.html',
            'templates/django_stachoutils/forms/widgets/*.html',
        ]
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
