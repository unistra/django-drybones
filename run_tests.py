# -*- coding: utf-8 -*-


import os
import sys

import django

os.environ['DJANGO_SETTINGS_MODULE'] = '{{ project_name }}.settings.unittest'
django.setup()

from django.test.runner import DiscoverRunner


"""
Run tests script
"""

test_runner = DiscoverRunner(pattern='tests.py', verbosity=2,
                             interactive=True, failfast=False)

failures = test_runner.run_tests(['{{ project_name }}'])
sys.exit(failures)
