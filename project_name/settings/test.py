from .base import *


#######################
# Debug configuration #
#######################

DEBUG = True


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
