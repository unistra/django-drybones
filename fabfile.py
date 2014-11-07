# -*- coding: utf-8 -*-

"""
"""

from fabric.api import (env, roles, execute, task)
from os.path import join

import pydiploy

# edit config here !
env.user = 'root'  # user for ssh

env.remote_owner = 'django'  # remote server user
env.remote_group = 'di'  # remote server group

env.application_name = '{{ project_name }}'   # name of webapp
env.root_package_name = '{{ project_name }}'  # name of app in webapp

env.remote_home = '/home/django'  # remote home root
env.remote_python_version = ''  # python version
env.remote_virtualenv_root = join(env.remote_home, '.virtualenvs')  # venv root
env.remote_virtualenv_dir = join(env.remote_virtualenv_root,
                                 env.application_name)  # venv for webapp dir
env.remote_repo_url = 'git@git.net:{{ project_name }}.git'  # git repository url
env.local_tmp_dir = '/tmp'  # tmp dir
env.remote_static_root = '/var/www/static/'  # root of static files
env.locale = 'fr_FR.UTF-8'  # locale to use on remote
env.timezone = 'Europe/Paris'  # timezone for remote
env.keep_releases = 2  # number of old releases to keep before cleaning

env.dipstrap_version = 'latest'
# env.oracle_client_version = '11.2'
# env.oracle_download_url = 'http://librepo.net/lib/oracle/'
# env.oracle_remote_dir = 'oracle_client'
# env.oracle_packages = ['instantclient-basic-linux-x86-64-11.2.0.2.0.zip',
#                        'instantclient-sdk-linux-x86-64-11.2.0.2.0.zip',
#                        'instantclient-sqlplus-linux-x86-64-11.2.0.2.0.zip']


@task
def dev():
    """Define dev stage"""
    env.roledefs = {
        'web': ['192.168.1.2'],
        'lb': ['192.168.1.2'],
    }
    env.backends = env.roledefs['web']
    env.server_name = '{{ project_name }}-dev.net'
    env.short_server_name = '{{ project_name }}-dev'
    env.static_folder = '/site_media/'
    env.server_ip = '192.168.1.2'
    env.no_shared_sessions = False
    env.server_ssl_on = False
    env.goal = 'dev'
    env.socket_port = '8001'
    env.map_settings = {}
    execute(build_env)


@task
def test():
    """Define test stage"""
    env.roledefs = {
        'web': ['{{ project_name }}-test.net'],
        'lb': ['lb.{{ project_name }}-test.net'],
    }
    env.backends = ['127.0.0.1']
    env.server_name = '{{ project_name }}-test.net'
    env.short_server_name = '{{ project_name }}-test'
    env.static_folder = '/site_media/'
    env.server_ip = ''
    env.no_shared_sessions = False
    env.server_ssl_on = False
    env.path_to_cert = '/etc/ssl/certs/{{ project_name }}.net.pem'
    env.path_to_cert_key = '/etc/ssl/private/{{ project_name }}.net.key'
    env.goal = 'test'
    env.socket_port = ''
    env.map_settings = {}
    execute(build_env)


@task
def preprod():
    """Define preprod stage"""
    env.roledefs = {
        'web': ['{{ project_name }}-pprd.net'],
        'lb': ['lb.{{ project_name }}-pprd.net'],
    }
    env.backends = env.roledefs['web']
    env.server_name = '{{ project_name }}-pprd.net'
    env.short_server_name = '{{ project_name }}-pprd'
    env.static_folder = '/site_media/'
    env.server_ip = ''
    env.no_shared_sessions = False
    env.server_ssl_on = True
    env.path_to_cert = '/etc/ssl/certs/{{ project_name }}.net.pem'
    env.path_to_cert_key = '/etc/ssl/private/{{ project_name }}.net.key'
    env.goal = 'preprod'
    env.socket_port = ''
    env.map_settings = {
        'default_db_host': "DATABASES['default']['HOST']",
        'default_db_user': "DATABASES['default']['USER']",
        'default_db_password': "DATABASES['default']['PASSWORD']",
        'default_db_name': "DATABASES['default']['NAME']",
        'secret_key': "SECRET_KEY",
    }
    execute(build_env)


@task
def prod():
    """Define prod stage"""
    env.roledefs = {
        'web': ['{{ project_name }}.net'],
        'lb': ['lb.{{ project_name }}.net']
    }
    env.backends = env.roledefs['web']
    env.server_name = '{{ project_name }}.net'
    env.short_server_name = '{{ project_name }}'
    env.static_folder = '/site_media/'
    env.server_ip = ''
    env.no_shared_sessions = False
    env.server_ssl_on = True
    env.path_to_cert = '/etc/ssl/certs/{{ project_name }}.net.pem'
    env.path_to_cert_key = '/etc/ssl/private/{{ project_name }}.net.key'
    env.goal = 'prod'
    env.socket_port = ''
    env.map_settings = {
        'default_db_host': "DATABASES['default']['HOST']",
        'default_db_user': "DATABASES['default']['USER']",
        'default_db_password': "DATABASES['default']['PASSWORD']",
        'default_db_name': "DATABASES['default']['NAME']",
        'secret_key': "SECRET_KEY",
    }
    execute(build_env)

# dont touch after that point if you don't know what you are doing !


@task
def tag(version_number):
    """ Set the version to deploy to `version_number`. """
    execute(pydiploy.prepare.tag, version=version_number)


@roles(['web', 'lb'])
def build_env():
    execute(pydiploy.prepare.build_env)


@task
def pre_install():
    """Pre install of backend & frontend"""
    execute(pre_install_backend)
    execute(pre_install_frontend)


@roles('web')
@task
def pre_install_backend():
    """Setup server for backend"""
    execute(pydiploy.django.pre_install_backend, commands='/usr/bin/rsync')


@roles('lb')
@task
def pre_install_frontend():
    """Setup server for frontend"""
    execute(pydiploy.django.pre_install_frontend)


@roles('web')
@task
def deploy(update_pkg=False):
    """Deploy code on server"""
    execute(deploy_backend)
    execute(deploy_frontend)


@roles('web')
@task
def deploy_backend(update_pkg=False):
    """Deploy code on server"""
    execute(pydiploy.django.deploy_backend)


@roles('lb')
@task
def deploy_frontend():
    """Deploy static files on load balancer"""
    execute(pydiploy.django.deploy_frontend)


@roles('web')
@task
def rollback():
    """Rollback code (current-1 release)"""
    execute(pydiploy.django.rollback)


@task
def post_install():
    """post install for backend & frontend"""
    execute(post_install_backend)
    execute(post_install_frontend)


@roles('web')
@task
def post_install_backend():
    """Post installation of backend"""
    execute(pydiploy.django.post_install_backend)


@roles('lb')
@task
def post_install_frontend():
    """Post installation of frontend"""
    execute(pydiploy.django.post_install_frontend)


@roles('web')
@task
def install_postgres():
    """Install Postgres on remote"""
    execute(pydiploy.require.database.install_postgres_server)


@task
def reload():
    """Reload backend & frontend"""
    execute(reload_frontend)
    execute(reload_backend)


@roles('lb')
@task
def reload_frontend():
    execute(pydiploy.django.reload_frontend)


@roles('web')
@task
def reload_backend():
    execute(pydiploy.django.reload_backend)
