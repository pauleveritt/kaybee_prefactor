from kaybee.references import BaseReference
from kaybee.registry import registry


@registry.resource('category')
class Category(BaseReference):
    pass
