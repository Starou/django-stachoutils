import os

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = 'i0_+-t@@wul&q)30+4y)8-19s)31@%cv8$q(c@8q1g#h$6wn-='

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',
]

MEDIA_URL = 'http://media.my_project.com/'
MEDIA_ROOT = os.path.join(CURRENT_DIR, 'media')

THUMBOR_SERVER = 'http://my_thumbor.com:8888'
THUMBOR_SERVER_EXTERNAL = THUMBOR_SERVER

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/django_mail'
#EMAIL_HOST = 'smtp'
EMAIL_SUBJECT_PREFIX = "[DJANGO PROJECT] "

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s',
        },
    },
    'handlers': {
        'null': {
            'level': 'ERROR',
            'class': 'django_stachoutils.log.NullHandler',
        },
        'message': {
            'level': 'WARNING',
            'class': 'django_stachoutils.log.MessagelHandler',
            'formatter': 'simple'
        },
        'mail_admins_buffered': {
            'level': 'INFO',
            'class': 'django_stachoutils.log.BufferingAdminEmailHandler',
            'subject': "[MY PROJECT]",
        },
        'mail_admins': {
            'level': 'INFO',
            'class': 'django_stachoutils.log.AdminEmailHandler',
            'subject': "[MY PROJECT]",
        },
    },
    'loggers': {
        'django.DisallowedHost': {
            'handlers': ['null'],
            'propagate': True,
        },
        'stachoutils.logger1': {
            'handlers': ['message'],
            'level': 'INFO',
            'propagate': True,
        },
    }
}
