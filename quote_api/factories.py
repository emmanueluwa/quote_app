# https://factoryboy.readthedocs.io/en/stable/orms.html

import factory
from . import models

class QuoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Quote
    
    name = factory.Faker('company')
    address = factory.Faker('address')
    description = factory.Faker('paragraph')
