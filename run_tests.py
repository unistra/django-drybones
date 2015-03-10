# -*- coding: utf-8 -*-


import os
import sys
import inspect

import django

os.environ['DJANGO_SETTINGS_MODULE'] = '{{ project_name }}.settings.unittest'
django.setup()

from django.test.runner import DiscoverRunner


"""
Run tests script
"""


def predicate(model, module_ends):
    return inspect.isclass(model) and model.__module__.endswith(module_ends)


def manage_model(model):
    model._meta.managed = True

test_runner = DiscoverRunner(pattern='tests.py', verbosity=2,
                             interactive=True, failfast=False)

failures = test_runner.run_tests(['{{ project_name }}'])
sys.exit(failures)
