from os import environ
from pathlib import Path

from .base import *

#######################
# Debug configuration #
#######################

DEBUG = True


##########################
# Database configuration #
##########################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': environ.get('DEFAULT_DB_TEST_NAME', '{{ project_name }}'),
        'USER': environ.get('DEFAULT_DB_TEST_USER', '{{ project_name }}'),
        'PASSWORD': environ.get('DEFAULT_DB_TEST_PASSWORD', '{{ project_name }}'),
        'HOST': environ.get('DEFAULT_DB_TEST_HOST', 'postgres'),
        'PORT': environ.get('DEFAULT_DB_TEST_PORT', ''),
    }
}

############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = ['*']

#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = environ.get(
    'LOG_DIR',
    Path('/tmp').resolve(strict=True) / f'test_{SITE_NAME}.log',
)
LOGGING['handlers']['file']['level'] = 'DEBUG'

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['level'] = 'DEBUG'

TEST_RUNNER = 'django.test.runner.DiscoverRunner'
