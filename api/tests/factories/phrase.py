import factory

from faker import Faker
from .user import UserFactory, TestUserFactory

en_faker = Faker(['en_US'])
jp_faker = Faker(['jp_JP'])


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
    text = en_faker.sentence(nb_words=8)
    text_language = 'en'
    translated_word = jp_faker.sentence(nb_words=8),
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
