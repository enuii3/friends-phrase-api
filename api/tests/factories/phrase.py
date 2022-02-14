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
    translated_word = faker.sentence(nb_words=8),

    @factory.post_generation
    def text_language(self, create, extracted, **kwargs):
        if not create:
            print(kwargs)
            return

        if extracted:
            self.text_language.add(extracted)

    @factory.post_generation
    def translated_word_language(self, create, extracted, **kwargs):
        if not create:
            print(kwargs)
            return

        if extracted:
            self.translated_word_language.add(extracted)


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
    translated_word = 'test_translated_word'

    @factory.post_generation
    def text_language(self, create, extracted, **kwargs):
        if not create:
            print(kwargs)
            return

        if extracted:
            self.text_language.add(extracted)

    @factory.post_generation
    def translated_word_language(self, create, extracted, **kwargs):
        if not create:
            print(kwargs)
            return

        if extracted:
            self.translated_word_language.add(extracted)
