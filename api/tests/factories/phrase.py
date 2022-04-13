import factory

from faker import Faker
from .user import UserFactory, TestUserFactory

faker = Faker(['en_US'])


class PhraseFactoryWith(factory.django.DjangoModelFactory):
    class Meta:
        model = 'api.Phrase'
        django_get_or_create = ('user',
                                'text',
                                'translated_word',
                                )

    user = factory.SubFactory(
        UserFactory,
    )
    text = faker.sentence(nb_words=8)
    text_language = 'en'
    translated_word = faker.sentence(nb_words=8),
    translated_word_language = 'jp'


class TestPhraseFactoryWith(factory.django.DjangoModelFactory):
    class Meta:
        model = 'api.Phrase'
        django_get_or_create = ('user',
                                'text',
                                'translated_word',
                                )

    user = factory.SubFactory(
        TestUserFactory,
    )
    text = 'test_text'
    text_language = 'en'
    translated_word_language = 'jp'
    translated_word = 'test_translated_word'
