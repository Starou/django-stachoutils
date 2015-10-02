import os
from distutils.core import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))


setup(
    name="django-stachoutils",
    version="2.0.1",
    license='BSD Licence',
    author='Stanislas Guerra',
    author_email='stan@slashdev.me',
    description='Commons for Django',
    url='https://github.com/Starou/django-stachoutils',
    long_description=README,
    packages=[
        'django_stachoutils',
        'django_stachoutils.management',
        'django_stachoutils.management.commands',
        'django_stachoutils.forms',
        'django_stachoutils.views',
        'django_stachoutils.templatetags',
    ],
    # I fucking hate distutils-wasting-time-machine.
    # python setup.py build does not give a shit about what is in MANIFEST.in
    # and here in package_data there is now fucking way to use ** glob style so
    # you have to maintain that fucking list.
    # A workaround is to use from setuptools import find_packages and
    # set include_package_data=True but in that case you cannot upload to Pypi!
    # Or maybe the doc sucks. Or maybe I am stupid.
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
        ]
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ]
)
