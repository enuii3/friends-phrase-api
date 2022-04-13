import factory
from .user import UserFactory, TestUserFactory
from .phrase import PhraseFactoryWith, TestPhraseFactoryWith
from faker import Faker

faker = Faker(['en_US'])


class CommentFactoryWith(factory.django.DjangoModelFactory):
    class Meta:
        model = 'api.comment'
        django_get_or_create = ('user', 'phrase', 'text')

    user = factory.SubFactory(
        UserFactory,
    )
    phrase = factory.SubFactory(
        PhraseFactoryWith,
    )
    text = faker.sentence(nb_words=8)
    text_language = 'jp'


class TestCommentFactoryWith(factory.django.DjangoModelFactory):
    class Meta:
        model = 'api.comment'
        django_get_or_create = ('user', 'phrase', 'text')

    user = factory.SubFactory(
        TestUserFactory,
    )
    phrase = factory.SubFactory(
        TestPhraseFactoryWith,
    )
    text = 'test_text'
    text_language = 'jp'
