import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'friends_phrase.settings')

django.setup()
from api.tests.factories.user import UserFactory
from api.tests.factories.profile import ProfileFactoryWith
from api.tests.factories.phrase import PhraseFactoryWith
from api.tests.factories.comment import CommentFactoryWith


def populate(n=10):
    for _ in range(n):
        phrase_user = UserFactory()
        ProfileFactoryWith(user=phrase_user)
        phrases = PhraseFactoryWith.create_batch(n, user=phrase_user)
        comment_user = UserFactory()
        CommentFactoryWith(user=comment_user, phrase=phrases[0])


if __name__ == "__main__":
    print('populating scripts')
    populate()
    print('populating complete')
