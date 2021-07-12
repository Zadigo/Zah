import logging
from importlib import import_module
from typing import Any

from jinja2.environment import Environment


class ServerConfig:
    def __init__(self):
        module = import_module('zah.config')
        module_dict = module.__dict__
        for key, value in module_dict.items():
            if key.isupper():
                setattr(self, key, value)

    def __getitem__(self, name):
        return getattr(self, name, None)

    def __call__(self, key: str, value: Any):
        setattr(self, key.upper(), value)

server_configuration = ServerConfig()


def get_template_backend(default_name='TEMPLATE_BACKEND') -> Environment:
    return getattr(server_configuration, default_name, None)


def create_logger(name='Zah'):
    logger = logging.getLogger(name)
    handler = logging.FileHandler('zah.log')
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    return logger

default_logger = create_logger()
