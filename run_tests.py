import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

os.environ['DJANGO_SETTINGS_MODULE'] = '{{ project_name }}.settings.unittest'
django.setup()



"""
Run tests script
"""

TestRunner = get_runner(settings)
test_runner = TestRunner(pattern='test_*.py', verbosity=2, interactive=True, failfast=False)

test_apps = list(settings.LOCAL_APPS)
test_apps = test_apps if len(sys.argv) <= 1 else sys.argv[1:]
failures = test_runner.run_tests(test_apps)
sys.exit(failures)
