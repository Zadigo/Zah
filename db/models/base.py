import copy

from zah.db.models.expressions import Expression
from zah.db.shortcuts import get_database_backend


class Query(Expression):
    @classmethod
    def copy(cls):
        instance = cls()
        return instance 


class Manager(Expression):
    def run_queryset(self, expression):
        items = self.parse_expressions(expression)
        backend = get_database_backend()
        
    
    def filter(self, **expression):
        self.run_queryset(expression)
        return Query.copy()


class BaseModel(type):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__
        return new_class(cls, name, bases, attrs)


class ModelMeta(metaclass=BaseModel):
    def __init__(self):
        pass
    
    manager = Manager()


class Model(ModelMeta):
    pass



class TestModel(Model):
    pass

m = TestModel().manager.filter(name__is='a', surname=1)
