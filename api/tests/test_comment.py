from django.test import TestCase
from unittest import mock
from datetime import datetime
from .factories.comment import TestCommentFactoryWith
from .factories.language import LanguageFactory
from .factories.phrase import TestPhraseFactoryWith
from .factories.user import TestUserFactory
from api.models import User, Phrase, Comment


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
        self.assertEqual(self.comment.created_at, self.mock_date)
        self.assertEqual(self.comment.updated_at, self.mock_date)

    def test_value_when_edit_each_value(self):
        self.assertEqual(self.comment.updated_at, self.mock_date)
        self.comment.text = self.updated_comment_text
        self.comment.text_language.set([self.test_ja])
        self.comment.user.username = self.updated_username
        self.comment.save()

        self.assertEqual(self.comment.text, self.updated_comment_text)
        self.assertEqual(self.comment.text_language.first(), self.test_ja)
        self.assertEqual(self.comment.user.username, self.updated_username)
        self.assertNotEqual(self.comment.updated_at.strftime("%Y-%m-%d"), '2022-02-13')

    def test_decrement_profile_when_delete_user(self):
        users = User.objects.all()
        phrases = Phrase.objects.all()
        comments = Comment.objects.all()

        self.assertEqual(len(users), 2)
        self.assertEqual(len(phrases), 1)
        self.assertEqual(len(comments), 1)

        comments[0].delete()
        users = User.objects.all()
        phrases = Phrase.objects.all()
        comments = Comment.objects.all()

        self.assertEqual(len(users), 2)
        self.assertEqual(len(phrases), 1)
        self.assertEqual(len(comments), 0)
