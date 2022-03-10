from django.test import TestCase
from datetime import datetime
from .factories.language import LanguageFactory
from .factories.phrase import TestPhraseFactoryWith
from .factories.user import TestUserFactory
from api.models import Phrase
from django.contrib.auth import get_user_model
from freezegun import freeze_time

DT = datetime(2022, 2, 22, 2, 22)


class PhraseModelTest(TestCase):
    @freeze_time(DT)
    def setUp(self):
        self.updated_text = 'updated_text'
        self.updated_translated_word = 'updated_translated_word'
        self.test_en = LanguageFactory(name='test_en')
        self.test_ja = LanguageFactory(name='test_ja')
        self.updated_username = 'updated_username'

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
        self.assertEqual(self.phrase.created_at, DT)
        self.assertEqual(self.phrase.updated_at, DT)

    def test_value_when_edit_each_value(self):
        self.assertEqual(self.phrase.created_at, DT)
        self.assertEqual(self.phrase.updated_at, DT)

        update_time = datetime(2022, 2, 23, 2, 22)
        with freeze_time(update_time):
            self.phrase.text = self.updated_text
            self.phrase.text_language.set([self.test_ja])
            self.phrase.translated_word = self.updated_translated_word
            self.phrase.translated_word_language.set([self.test_en])
            self.user.username = self.updated_username
            self.user.save()
            self.phrase.save()

        self.assertEqual(self.phrase.text, self.updated_text)
        self.assertEqual(self.phrase.text_language.first(), self.test_ja)
        self.assertEqual(self.phrase.translated_word, self.updated_translated_word)
        self.assertEqual(self.phrase.translated_word_language.first(), self.test_en)
        self.assertEqual(self.phrase.user.username, self.updated_username)
        self.assertEqual(self.phrase.created_at, DT)
        self.assertEqual(self.phrase.updated_at, update_time)

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
