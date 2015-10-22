# -*- coding: utf-8 -*-

from os import environ
from os.path import normpath
from .base import *

#######################
# Debug configuration #
#######################

DEBUG = True


##########################
# Database configuration #
##########################

DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'
DATABASES['default']['NAME'] = environ.get('DEFAULT_DB_NAME', '{{ project_name }}.db')


#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = '{% templatetag openvariable %} remote_current_path {% templatetag closevariable %}/log/app.log'

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['level'] = 'DEBUG'


############
# Dipstrap #
############

DIPSTRAP_VERSION = '{% templatetag openvariable %} dipstrap_version {% templatetag closevariable %}'
DIPSTRAP_STATIC_URL += '%s/' % DIPSTRAP_VERSION
