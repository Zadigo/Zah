from zah.db.models.fields import Field
from zah.db.models.base import Model

class TestModel(Model):
    name = Field()
