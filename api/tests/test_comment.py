from django.test import TestCase
from unittest import mock
from datetime import datetime
from .factories.comment import TestCommentFactoryWith
from .factories.language import LanguageFactory
from .factories.phrase import TestPhraseFactoryWith
from .factories.user import TestUserFactory
from api.models import Phrase, Comment
from django.contrib.auth import get_user_model


class PhraseModelTest(TestCase):
    def setUp(self):
        self.mock_date = datetime(2022, 2, 13, 3, 55, 18, 91811)
        self.test_en = LanguageFactory(name='en')
        self.test_ja = LanguageFactory(name='ja')
        self.updated_username = 'updated_username'
        self.updated_comment_text = 'updated_comment_text'

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = self.mock_date
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
        self.assertEqual(self.comment.phrase, self.phrase)
        self.assertEqual(self.comment.created_at, self.mock_date)
        self.assertEqual(self.comment.updated_at, self.mock_date)

    def test_value_when_edit_each_value(self):
        self.assertEqual(self.comment.created_at, self.mock_date)
        self.assertEqual(self.comment.updated_at, self.mock_date)

        self.comment.text = self.updated_comment_text
        self.comment.text_language.set([self.test_ja])
        self.comment_user.username = self.updated_username
        self.comment.save()

        self.assertEqual(self.comment.text, self.updated_comment_text)
        self.assertEqual(self.comment.text_language.first(), self.test_ja)
        self.assertEqual(self.comment.user.username, self.updated_username)
        self.assertEqual(self.comment.created_at.strftime("%Y-%m-%d"), '2022-02-13')
        self.assertNotEqual(self.comment.updated_at.strftime("%Y-%m-%d"), '2022-02-13')

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
