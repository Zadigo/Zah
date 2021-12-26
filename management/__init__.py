from importlib import import_module
import os
from functools import lru_cache
from typing import OrderedDict


@lru_cache(maxsize=1)
def collect_commands_paths():
    module = import_module('zah.management.commands')
    full_path, _, files = list(os.walk(module.__path__[0]))[0]
    return list(map(lambda f: os.path.join(full_path, f), files))


def load_command_class(name):
    """Loads the command module and tries to
    return a Command instance"""
    paths = collect_commands_paths()
    for path in paths:
        basename = os.path.basename(path)
        module_name, _ = basename.split('.')
        if module_name == name:
            try:
                module_object = import_module(f'zah.management.commands.{module_name}')
            except ImportError:
                raise
            else:
                break
    return module_object.Command()


class Utility:
    commands_registry = OrderedDict()
    
    def __init__(self):
        paths = collect_commands_paths()
        
        for path in paths:
            basename = os.path.basename(path)
            module_name, _ = basename.split('.')
            try:
                module_object = import_module(f'zah.management.commands.{module_name}')
            except ImportError:
                raise
            else:
                self.commands_registry.setdefault(module_name, module_object)
    
    @staticmethod
    def parse_tokens(argv):
        filename = argv[0]
        remaining_tokens = argv[1:]
        return filename, remaining_tokens
        
    def call_command(self, argv):
        filename, tokens = self.parse_tokens(argv)
        command = tokens.pop(0)
        
        try:
            module = self.commands_registry[command]
        except:
            raise KeyError('Command does not exist')
        
        from zah.management.base import BaseCommand
        
        command_object = getattr(module, 'Command')
        instance = command_object()
        if not isinstance(instance, BaseCommand):
            raise TypeError('Command should be an instance of BaseCommand')
        
        parser = instance.create_parser()
        namespace = parser.parse_args()
        instance.execute(namespace=namespace)


def execute_command_inline(argv):
    utility = Utility()
    utility.call_command(argv)
