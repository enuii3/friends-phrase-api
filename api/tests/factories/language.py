import factory
import random


class LanguageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'api.Language'
        django_get_or_create = ('name',)

    name = random.choice(
        ['ar', 'bg', 'bn', 'bs', 'cs', 'da',
         'de', 'dk', 'el', 'es', 'et', 'en',
         'fa', 'fi', 'fil', 'fr', 'ga', 'he',
         'hi', 'hr', 'hu', 'hy', 'id', 'it',
         'ka', 'ja', 'ko', 'la', 'lb', 'lt',
         'lv', 'mt', 'ne', 'nl', 'no', 'or',
         'pl', 'pt', 'ro', 'ru', 'sk', 'sl',
         'sv', 'ta', 'th', 'tl', 'tr', 'tw',
         'uk', 'zh']
    )
