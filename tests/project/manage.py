#!/usr/bin/env python

import os
import sys

from zah.management import execute_command_inline

if __name__ == '__main__':
    os.environ.setdefault('ZAH_WEB_PROJECT', 'zah.tests.project.settings')
    execute_command_inline(sys.argv)
