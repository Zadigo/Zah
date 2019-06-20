class BaseModel(type):
    def __new__(cls, name, bases, cls_dict, **kwargs):
        return super().__new__(cls, name, bases, cls_dict, **kwargs)

class Model(metaclass=BaseModel):
    def __init__(self):
        pass