import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friends_phrase.settings')

django.setup()
from api.tests.factories.language import LanguageFactory
from api.tests.factories.user import UserFactory
from api.tests.factories.profile import ProfileFactoryWith
from api.tests.factories.phrase import PhraseFactoryWith
from api.tests.factories.comment import CommentFactoryWith


def populate(n=10):
    for _ in range(n):
        language = LanguageFactory()
        phrase_user = UserFactory()
        ProfileFactoryWith(user=phrase_user)
        phrases = PhraseFactoryWith.create_batch(n, user=phrase_user,
                                                 text_language=language,
                                                 translated_word_language=language)
        comment_user = UserFactory()
        language = LanguageFactory()
        CommentFactoryWith(user=comment_user, phrase=phrases[0], text_language=language)


if __name__ == "__main__":
    print('populating scripts')
    populate()
    print('populating complete')
