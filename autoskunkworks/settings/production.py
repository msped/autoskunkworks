import os
from dotenv import load_dotenv
from .base import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

load_dotenv()

DEBUG = False


ALLOWED_HOSTS = [
    'localhost',
    'autoskunkworks.mspe.me',
    'https://autoskunkworks.mspe.me',
    '127.0.0.1'
]


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]

STATIC_URL = '/static/'
STATIC_ROOT = '/backend/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/backend/media/'

sentry_sdk.init(
    dsn=os.environ.get('SENTRY_DNS'),
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
