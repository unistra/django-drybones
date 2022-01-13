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

# In your virtualenv, edit the file $VIRTUAL_ENV/bin/postactivate and set
# properly the environnement variable defined in this file (ie: os.environ[KEY])
# ex: export DEFAULT_DB_NAME='project_name'

# Default values for default database are :
# engine : sqlite3
# name : PROJECT_ROOT_DIR/default.db


DATABASES = {
    'default': {
        'ENGINE': environ.get('DEFAULT_DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': environ.get('DEFAULT_DB_NAME', '{{ project_name }}'),
        'USER': environ.get('DEFAULT_DB_USER', '{{ project_name }}'),
        'PASSWORD': environ.get('DEFAULT_DB_PASSWORD', '{{ project_name }}'),
        'HOST': environ.get('DEFAULT_DB_HOST', 'localhost'),
        'PORT': environ.get('DEFAULT_DB_PORT', '5432'),
    }
}


############################
# Allowed hosts & Security #
############################

ALLOWED_HOSTS = ['*']


#####################
# Log configuration #
#####################

LOGGING['handlers']['file']['filename'] = environ.get('LOG_DIR', normpath(join('/tmp', '%s.log' % SITE_NAME)))
LOGGING['handlers']['file']['level'] = 'DEBUG'

for logger in LOGGING['loggers']:
    LOGGING['loggers'][logger]['level'] = 'DEBUG'


###########################
# Unit test configuration #
###########################

INSTALLED_APPS += [
    'coverage',
    'debug_toolbar',
]


############
# Dipstrap #
############

DIPSTRAP_VERSION = environ.get('DIPSTRAP_VERSION', 'latest')
DIPSTRAP_STATIC_URL += '%s/' % DIPSTRAP_VERSION


#################
# Debug toolbar #
#################

DEBUG_TOOLBAR_PATCH_SETTINGS = False
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
INTERNAL_IPS = ['127.0.0.1', '0.0.0.0']
