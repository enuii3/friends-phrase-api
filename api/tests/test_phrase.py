from django.test import TestCase
from unittest import mock
from datetime import datetime
from .factories.language import LanguageFactory
from .factories.phrase import TestPhraseFactoryWith
from .factories.user import TestUserFactory
from api.models import Phrase
from django.contrib.auth import get_user_model


class PhraseModelTest(TestCase):
    def setUp(self):
        self.updated_text = 'updated_text'
        self.updated_translated_word = 'updated_translated_word'
        self.mock_date = datetime(2022, 2, 13, 3, 55, 18, 91811)
        self.test_en = LanguageFactory(name='en')
        self.test_ja = LanguageFactory(name='ja')
        self.updated_username = 'updated_username'

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = self.mock_date
            self.user = TestUserFactory()
            self.phrase = TestPhraseFactoryWith(user=self.user,
                                                text_language=self.test_en,
                                                translated_word_language=self.test_ja
                                                )

    def test_basic_values(self):
        self.assertEqual(self.phrase.text, 'test_text')
        self.assertEqual(self.phrase.text_language.first(), self.test_en)
        self.assertEqual(self.phrase.translated_word, 'test_translated_word')
        self.assertEqual(self.phrase.translated_word_language.first(), self.test_ja)
        self.assertEqual(self.phrase.created_at, self.mock_date)
        self.assertEqual(self.phrase.updated_at, self.mock_date)

    def test_value_when_edit_each_value(self):
        self.assertEqual(self.phrase.created_at, self.mock_date)
        self.assertEqual(self.phrase.updated_at, self.mock_date)

        self.phrase.text = self.updated_text
        self.phrase.text_language.set([self.test_ja])
        self.phrase.translated_word = self.updated_translated_word
        self.phrase.translated_word_language.set([self.test_en])
        self.user.username = self.updated_username
        self.phrase.save()

        self.assertEqual(self.phrase.text, self.updated_text)
        self.assertEqual(self.phrase.text_language.first(), self.test_ja)
        self.assertEqual(self.phrase.translated_word, self.updated_translated_word)
        self.assertEqual(self.phrase.translated_word_language.first(), self.test_en)
        self.assertEqual(self.phrase.user.username, self.updated_username)
        self.assertEqual(self.phrase.created_at.strftime("%Y-%m-%d"), '2022-02-13')
        self.assertNotEqual(self.phrase.updated_at.strftime("%Y-%m-%d"), '2022-02-13')

    def test_decrement_phrase_when_delete_user(self):
        user_count = get_user_model().objects.count()
        phrase_count = Phrase.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(phrase_count, 1)

        get_user_model().objects.first().delete()

        user_count = get_user_model().objects.count()
        phrase_count = Phrase.objects.count()

        self.assertEqual(user_count, 0)
        self.assertEqual(phrase_count, 0)

    def test_decrement_phrase_when_delete_phrase(self):
        user_count = get_user_model().objects.count()
        phrase_count = Phrase.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(phrase_count, 1)

        Phrase.objects.first().delete()

        user_count = get_user_model().objects.count()
        phrase_count = Phrase.objects.count()

        self.assertEqual(user_count, 1)
        self.assertEqual(phrase_count, 0)
