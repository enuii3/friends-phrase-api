from django.test import TestCase
from datetime import datetime
from .factories.comment import TestCommentFactoryWith
from .factories.language import LanguageFactory
from .factories.phrase import TestPhraseFactoryWith
from .factories.user import TestUserFactory
from api.models import Phrase, Comment
from django.contrib.auth import get_user_model
from freezegun import freeze_time

DT = datetime(2022, 2, 22, 2, 22)


class CommentModelTest(TestCase):
    @freeze_time(DT)
    def setUp(self):
        self.test_en = LanguageFactory(name='test_en')
        self.test_ja = LanguageFactory(name='test_ja')
        self.updated_username = 'updated_username'
        self.updated_comment_text = 'updated_comment_text'

        self.phrase_user = TestUserFactory(username='phrase_user', email='phrase_user@sample.com')
        self.comment_user = TestUserFactory(username='comment_user', email='comment_user@sample.com')
        self.phrase = TestPhraseFactoryWith(user=self.phrase_user,
                                            text_language=self.test_en,
                                            translated_word_language=self.test_ja
                                            )
        self.comment = TestCommentFactoryWith(user=self.comment_user,
                                              phrase=self.phrase,
                                              text_language=self.test_en
                                              )

    def test_basic_values(self):
        self.assertEqual(self.comment.text, 'test_text')
        self.assertEqual(self.comment.text_language.first(), self.test_en)
        self.assertEqual(self.comment.user, self.comment_user)
        self.assertEqual(self.comment.phrase, self.phrase)
        self.assertEqual(self.comment.created_at, DT)
        self.assertEqual(self.comment.updated_at, DT)

    def test_value_when_edit_each_value(self):
        self.assertEqual(self.comment.created_at, DT)
        self.assertEqual(self.comment.updated_at, DT)

        update_time = datetime(2022, 2, 23, 2, 22)
        with freeze_time(update_time):
            self.comment.text = self.updated_comment_text
            self.comment.text_language.set([self.test_ja])
            self.comment_user.username = self.updated_username
            self.comment.save()

        self.assertEqual(self.comment.text, self.updated_comment_text)
        self.assertEqual(self.comment.text_language.first(), self.test_ja)
        self.assertEqual(self.comment.user.username, self.updated_username)
        self.assertEqual(self.comment.created_at, DT)
        self.assertEqual(self.comment.updated_at, update_time)

    def test_decrement_comment_when_delete_user(self):
        user_count = get_user_model().objects.count()
        phrase_count = Phrase.objects.count()
        comment_count = Comment.objects.count()
        self.assertEqual(user_count, 2)
        self.assertEqual(phrase_count, 1)
        self.assertEqual(comment_count, 1)

        get_user_model().objects.get(id=self.phrase_user.id).delete()

        user_count = get_user_model().objects.count()
        phrase_count = Phrase.objects.count()
        comment_count = Comment.objects.count()

        self.assertEqual(user_count, 1)
        self.assertEqual(phrase_count, 0)
        self.assertEqual(comment_count, 0)

    def test_decrement_comment_when_delete_phrase(self):
        user_count = get_user_model().objects.count()
        phrase_count = Phrase.objects.count()
        comment_count = Comment.objects.count()
        self.assertEqual(user_count, 2)
        self.assertEqual(phrase_count, 1)
        self.assertEqual(comment_count, 1)

        Phrase.objects.first().delete()

        user_count = get_user_model().objects.count()
        phrase_count = Phrase.objects.count()
        comment_count = Comment.objects.count()

        self.assertEqual(user_count, 2)
        self.assertEqual(phrase_count, 0)
        self.assertEqual(comment_count, 0)

    def test_decrement_comment_when_delete_comment(self):
        user_count = get_user_model().objects.count()
        phrase_count = Phrase.objects.count()
        comment_count = Comment.objects.count()
        self.assertEqual(user_count, 2)
        self.assertEqual(phrase_count, 1)
        self.assertEqual(comment_count, 1)

        Comment.objects.first().delete()

        user_count = get_user_model().objects.count()
        phrase_count = Phrase.objects.count()
        comment_count = Comment.objects.count()

        self.assertEqual(user_count, 2)
        self.assertEqual(phrase_count, 1)
        self.assertEqual(comment_count, 0)
