import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friends_phrase.settings')

import django
django.setup()
from api.tests.factories.language import LanguageFactory
from api.tests.factories.user import UserFactory
from api.tests.factories.profile import ProfileFactoryWith
from api.tests.factories.phrase import PhraseFactoryWith
from api.tests.factories.comment import CommentFactoryWith


def populate(n=2):
    for _ in range(n):
        language = LanguageFactory()
        phrase_user = UserFactory(username='factory_user1', email='factory1@sample.com')
        ProfileFactoryWith(user=phrase_user)
        phrase = PhraseFactoryWith(user=phrase_user,
                                   text_language=language,
                                   translated_word_language=language)
        comment_user = UserFactory(username='factory_user2', email='factory2@sample.com')
        language = LanguageFactory()
        CommentFactoryWith(user=comment_user, phrase=phrase, text_language=language)


if __name__ == "__main__":
    print('populating scripts')
    populate()
    print('populating complete')
