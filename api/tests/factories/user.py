import factory
from faker import Faker

faker = Faker(['en_US'])


class UserFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = 'api.User'
        django_get_or_create = ('username', 'email', 'password')

    username = faker.name()
    email = faker.email()
    password = faker.password


class TestUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'api.User'
        django_get_or_create = ('username', 'email', 'password')

    username = 'test_username'
    email = 'test_email@sample.com'
    password = faker.password
