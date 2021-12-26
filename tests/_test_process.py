import os
import subprocess
import sys

from zah.management import execute_command_inline

if __name__ == '__main__':
    os.environ.setdefault('ZAH_WEB_PROJECT', 'zah.tests.project.settings')
    subprocess.call(['python', 'tests/project/manage.py', 'run_server'], stderr=subprocess.STDOUT)
    execute_command_inline(sys.argv)
