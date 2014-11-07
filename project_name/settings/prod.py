# -*- coding: utf-8 -*-

from os import environ
from os.path import normpath

from .base import *


##########################
# Database configuration #
##########################

DATABASES['default']['HOST'] = '{% templatetag openvariable %} default_db_host {% templatetag closevariable %}'
DATABASES['default']['USER'] = '{% templatetag openvariable %} default_db_user {% templatetag closevariable %}'
DATABASES['default']['PASSWORD'] = '{% templatetag openvariable %} default_db_password {% templatetag closevariable %}'
DATABASES['default']['NAME'] = '{% templatetag openvariable %} default_db_name {% templatetag closevariable %}'


############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = [
    '.u-strasbg.fr',
    '.unistra.fr',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTOCOL', 'ssl')


#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = '{% templatetag openvariable %} remote_current_path {% templatetag closevariable %}/log/app.log'

##############
# Secret key #
##############

SECRET_KEY = '{% templatetag openvariable %} secret_key {% templatetag closevariable %}'


############
# Dipstrap #
############

DIPSTRAP_STATIC_URL += '%s/' % DIPSTRAP_VERSION
