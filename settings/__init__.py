from importlib import import_module
import os

PROJECT_ENVIRON_NAME = 'ZAH_WEB_PROJECT'

class UserSettings:
    SETTINGS_MODULE = None
    
    def __init__(self):
        self.configured = False
        dotted_path = os.environ.get(PROJECT_ENVIRON_NAME, None)
        
        if dotted_path is not None:
            self.SETTINGS_MODULE = import_module(dotted_path)
            settings_module_dict = self.SETTINGS_MODULE.__dict__
            for key, value in settings_module_dict.items():
                if key.isupper():
                    setattr(self, key, value)
            self.configured = True
            
    @property
    def is_configured(self):
        return self.configured
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(configured={self.configured})"
    
    def __getitem__(self, name):
        return getattr(self, name, None)
    
    def __setitem__(self, name):
        return setattr(self, name)
    

class Settings:
    def __init__(self):
        global_settings = import_module('zah.settings.base')
        global_settings_dict = global_settings.__dict__
        for key, value in global_settings_dict.items():
            if key.isupper():
                setattr(self, key, value)
        
        requires_list = ['TEMPLATES']
        user_settings = UserSettings()
        for key, value in user_settings.__dict__.items():
            user_setting = user_settings[key]
            
            if key in requires_list:
                if isinstance(value, list):
                    global_setting = getattr(self, key, [])
                    global_setting.extend(value)
                    user_setting = global_setting
            
            setattr(self, key, user_setting)
        self.user_settings = user_settings
            
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.user_settings})"
    
    def __str__(self):
        return str(self.__dict__)

    def __call__(self, **settings):
        self.__init__()
        for key, value in settings.items():
            if not key.isupper():
                key = key.upper()
            setattr(self, key, value)
        return self
    
    def __setitem__(self, key, value):
        self.__dict__[key] = value


class LazySettings:
    pass

settings = Settings()
