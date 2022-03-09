# https://factoryboy.readthedocs.io/en/stable/orms.html

import factory
from . import models
from django.contrib.auth.models import User

class QuoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Quote
    
    name = factory.Faker('company')
    address = factory.Faker('address')
    description = factory.Faker('paragraph')

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker("word")
    email = factory.Faker("email")
    is_active = True
    #password will be hashed when it gets to db
    password = factory.PostGenerationMethodCall("set_password", "password123")
