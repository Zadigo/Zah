import os
import pathlib

class Configuration:
    def __init__(self):
        # Base path
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Templates path
        self.templates_path = os.path.join(self.base_path, 'templates')
