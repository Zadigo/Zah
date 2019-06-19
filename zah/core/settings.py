import os
import pathlib
import sys

def root_path(module):
    module = os.path.dirname(os.path.abspath(module))
    if module:
        return list(os.walk(module))[0][0]

# def templates_path(module):
#     module = os.path.dirname(os.path.abspath(module))
#     if module:
#         items = os.walk(module)
#         for item in items:
#             if os.path.basename(item[0]) == 'templates':
#                 path_dir['templates'] = item

class Configuration(dict):
    def __init__(self, **kwargs):
        # Base path
        self.base_path = root_path(kwargs['module'])
        # Templates path
        self.templates_path = os.path.join(self.base_path, 'templates')



# print(list(os.walk(os.path.dirname(os.path.abspath(__file__)))))