#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "strongly_typed_wagtail.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

#from home.views import generate_daily_advice
#generate_daily_advice()
