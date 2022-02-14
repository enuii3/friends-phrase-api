import factory
import random
from .user import UserFactory, TestUserFactory
from faker import Faker

faker = Faker(['en_US'])


class ProfileFactoryWith(factory.django.DjangoModelFactory):
    class Meta:
        model = 'api.Profile'
        django_get_or_create = ('user', 'sex', 'date_of_birth')

    user = factory.SubFactory(
        UserFactory,
    )
    sex = random.choice(['men', 'women', 'another'])
    date_of_birth = faker.date()


class TestProfileFactoryWith(factory.django.DjangoModelFactory):
    class Meta:
        model = 'api.Profile'
        django_get_or_create = ('user', 'sex', 'date_of_birth')

    user = factory.SubFactory(
        TestUserFactory,
    )
    sex = 'men'
    date_of_birth = '1993-05-01'
