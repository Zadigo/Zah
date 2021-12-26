class BaseModel(type):
    def __new__(cls, name, bases, attrs):
        new_class = super.__new__
        return new_class(cls, name, bases, attrs) 


class ModelMeta(metaclass=BaseModel):
    def __init__(self):
        pass


class Model(ModelMeta):
    pass
