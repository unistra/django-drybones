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

test_runner = DiscoverRunner(pattern='test_*.py', verbosity=2,
                             interactive=True, failfast=False)

test_apps = ['{{ project_name }}']
test_apps = test_apps if len(sys.argv) <= 1 else sys.argv[1:]
failures = test_runner.run_tests(test_apps)
sys.exit(failures)
