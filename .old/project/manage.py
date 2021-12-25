import os

def execute_inline(argv):
    os.environ.setdefault('ZAH_APP', 'project.app')
    