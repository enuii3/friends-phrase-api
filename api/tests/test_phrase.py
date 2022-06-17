from django.test import TestCase
from django.urls import reverse
from datetime import datetime
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from .factories.phrase import TestPhraseFactoryWith, PhraseFactoryWith
from .factories.user import TestUserFactory, UserFactory
from api.models import Phrase
from django.contrib.auth import get_user_model
from freezegun import freeze_time
from api.serializers import PhraseSerializer

DT = datetime(2022, 2, 22, 2, 22)
UPDATE_DT = datetime(2022, 3, 22, 2, 22)
CREATE_PHRASE_URL = '/api/phrase/'


def detail_phrase_url(phrase_id):
    return reverse('api:phrase-detail', args=[phrase_id])


class PhraseApiTest(APITestCase):
    def setUp(self):
        self.user = TestUserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_should_create_phrase(self):
        payload = {'text': 'test_text',
                   'text_language': 'en',
                   'translated_word': 'テスト テキスト',
                   'translated_word_language': 'jp',
                   }

        self.assertEqual(Phrase.objects.count(), 0)
        with freeze_time(DT):
            res = self.client.post(CREATE_PHRASE_URL, payload)

        phrase = Phrase.objects.get(id=res.data['id'])
        self.assertEqual(Phrase.objects.count(), 1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(phrase.text, payload['text'])
        self.assertEqual(phrase.text_language, payload['text_language'])
        self.assertEqual(phrase.translated_word, payload['translated_word'])
        self.assertEqual(phrase.translated_word_language, payload['translated_word_language'])
        self.assertEqual(phrase.created_at, DT)
        self.assertEqual(phrase.updated_at, DT)
        self.assertEqual(phrase.user, self.user)
        self.assertEqual(phrase.comments.count(), 0)


def test_should_not_create_phrase_by_blank_value(self):
    payload = {'text': '',
               'text_language': '',
               'translated_word': '',
               'translated_word_language': '',
               }
    res = self.client.post(CREATE_PHRASE_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(res.data['text'][0], 'This field may not be blank.')
    self.assertEqual(res.data['text_language'][0], '“” is not a valid UUID.')
    self.assertEqual(res.data['translated_word'][0], 'This field may not be blank.')
    self.assertEqual(res.data['translated_word_language'][0], '“” is not a valid UUID.')


def test_should_not_create_phrase_by_missing_key(self):
    payload = {'missing_text': 'test_text',
               'missing_text_language': self.test_en.id,
               'missing_translated_word': 'テスト テキスト',
               'missing_translated_word_language': self.test_ja.id,
               }
    res = self.client.post(CREATE_PHRASE_URL, payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(res.data['text'][0], 'This field is required.')
    self.assertEqual(res.data['text_language'][0], 'This list may not be empty.')
    self.assertEqual(res.data['translated_word'][0], 'This field is required.')
    self.assertEqual(res.data['translated_word_language'][0], 'This list may not be empty.')


def test_should_update_phrase(self):
    update_payload = {'text': 'update_text',
                      'text_language': self.test_ja.id,
                      'translated_word': '編集済のテキスト',
                      'translated_word_language': self.test_en.id,
                      }
    with freeze_time(DT):
        phrase = TestPhraseFactoryWith(user=self.user,
                                       text_language=self.test_en.id,
                                       translated_word_language=self.test_ja.id)
    with freeze_time(UPDATE_DT):
        res = self.client.put(detail_phrase_url(phrase.id), update_payload)
    phrase.refresh_from_db()

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(phrase.text, update_payload['text'])
    self.assertEqual(phrase.text_language.first().id, update_payload['text_language'])
    self.assertEqual(phrase.translated_word, update_payload['translated_word'])
    self.assertEqual(phrase.translated_word_language.first().id, update_payload['translated_word_language'])
    self.assertEqual(phrase.created_at, DT)
    self.assertEqual(phrase.updated_at, UPDATE_DT)
    self.assertEqual(phrase.user, self.user)
    self.assertEqual(phrase.comments.count(), 0)


def test_should_not_update_phrase_with_not_owner(self):
    update_payload = {'text': 'update_text',
                      'text_language': self.test_ja.id,
                      'translated_word': 'update_translated_word',
                      'translated_word_language': self.test_en.id,
                      }
    another_user = UserFactory(username='another_user', email='another_user@sample.com', password='another_pw')
    another_phrase = TestPhraseFactoryWith(user=another_user,
                                           text_language=self.test_en.id,
                                           translated_word_language=self.test_ja.id)
    res = self.client.put(detail_phrase_url(another_phrase.id), update_payload)

    self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    self.assertEqual(res.data['detail'], 'You do not have permission to perform this action.')


def test_should_not_update_phrase_by_blank_value(self):
    update_payload = {
        'text': '',
        'text_language': '',
        'translated_word': '',
        'translated_word_language': '',
    }
    phrase = PhraseFactoryWith(user=self.user)
    res = self.client.put(detail_phrase_url(phrase.id), update_payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(res.data['text'][0], 'This field may not be blank.')
    self.assertEqual(res.data['text_language'][0], '“” is not a valid UUID.')
    self.assertEqual(res.data['translated_word'][0], 'This field may not be blank.')
    self.assertEqual(res.data['translated_word_language'][0], '“” is not a valid UUID.')


def test_should_not_update_phrase_by_missing_key(self):
    update_payload = {'missing_text': 'test_text',
                      'missing_text_language': self.test_en.id,
                      'missing_translated_word': 'テスト テキスト',
                      'missing_translated_word_language': self.test_ja.id,
                      }
    phrase = PhraseFactoryWith(user=self.user,
                               text_language=self.test_ja.id,
                               translated_word_language=self.test_en.id)
    res = self.client.put(detail_phrase_url(phrase.id), update_payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(res.data['text'][0], 'This field is required.')
    self.assertEqual(res.data['text_language'][0], 'This list may not be empty.')
    self.assertEqual(res.data['translated_word'][0], 'This field is required.')
    self.assertEqual(res.data['translated_word_language'][0], 'This list may not be empty.')


def test_should_not_update_phrase_with_not_exists(self):
    update_payload = {
        'text': 'update_text',
        'text_language': self.test_ja.id,
        'translated_word': 'update_translated_word',
        'translated_word_language': self.test_en.id,
    }
    phrase = PhraseFactoryWith(user=self.user,
                               text_language=self.test_ja.id,
                               translated_word_language=self.test_en.id)

    not_exists_url = detail_phrase_url(phrase.id) + '1'
    res = self.client.put(not_exists_url, update_payload)

    self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


def test_should_partial_update_phrase(self):
    partial_update_payload = {'text': 'partial_update_text',
                              'text_language': self.test_ja.id,
                              'translated_word': '編集済のテキスト',
                              'translated_word_language': self.test_en.id,
                              }
    with freeze_time(DT):
        phrase = TestPhraseFactoryWith(user=self.user,
                                       text_language=self.test_en.id,
                                       translated_word_language=self.test_ja.id)
    with freeze_time(UPDATE_DT):
        res = self.client.patch(detail_phrase_url(phrase.id), partial_update_payload)
    phrase.refresh_from_db()

    self.assertEqual(res.status_code, status.HTTP_200_OK)
    self.assertEqual(phrase.text, partial_update_payload['text'])
    self.assertEqual(phrase.text_language.first().id, partial_update_payload['text_language'])
    self.assertEqual(phrase.translated_word, partial_update_payload['translated_word'])
    self.assertEqual(phrase.translated_word_language.first().id, partial_update_payload['translated_word_language'])
    self.assertEqual(phrase.created_at, DT)
    self.assertEqual(phrase.updated_at, UPDATE_DT)
    self.assertEqual(phrase.user, self.user)
    self.assertEqual(phrase.comments.count(), 0)


def test_should_not_partial_update_phrase_with_not_owner(self):
    partial_update_payload = {'text': 'partial_update_text',
                              'text_language': self.test_ja.id,
                              'translated_word': 'partial_update_translated_word',
                              'translated_word_language': self.test_en.id,
                              }
    another_user = UserFactory(username='another_user', email='another_user@sample.com', password='another_pw')
    another_phrase = TestPhraseFactoryWith(user=another_user,
                                           text_language=self.test_en.id,
                                           translated_word_language=self.test_ja.id)
    res = self.client.patch(detail_phrase_url(another_phrase.id), partial_update_payload)

    self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    self.assertEqual(res.data['detail'], 'You do not have permission to perform this action.')


def test_should_not_partial_update_phrase_by_blank_value(self):
    partial_update_payload = {
        'text': '',
        'text_language': '',
        'translated_word': '',
        'translated_word_language': '',
    }
    phrase = PhraseFactoryWith(user=self.user)
    res = self.client.patch(detail_phrase_url(phrase.id), partial_update_payload)

    self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    self.assertEqual(res.data['text'][0], 'This field may not be blank.')
    self.assertEqual(res.data['text_language'][0], '“” is not a valid UUID.')
    self.assertEqual(res.data['translated_word'][0], 'This field may not be blank.')
    self.assertEqual(res.data['translated_word_language'][0], '“” is not a valid UUID.')


def test_should_not_partial_update_phrase_by_missing_key(self):
    partial_update_payload = {'missing_text': 'test_text',
                              'missing_text_language': self.test_en.id,
                              'missing_translated_word': 'テスト テキスト',
                              'missing_translated_word_language': self.test_ja.id,
                              }
    phrase = PhraseFactoryWith(user=self.user,
                               text='test_text',
                               text_language=self.test_ja.id,
                               translated_word='テスト テキスト',
                               translated_word_language=self.test_en.id)
    self.client.patch(detail_phrase_url(phrase.id), partial_update_payload)

    self.assertEqual(phrase.text, 'test_text')
    self.assertEqual(phrase.text_language.first(), self.test_ja)
    self.assertEqual(phrase.translated_word, 'テスト テキスト')
    self.assertEqual(phrase.translated_word_language.first(), self.test_en)


def test_should_not_partial_update_phrase_with_not_exists(self):
    partial_update_payload = {
        'text': 'partial_update_text',
        'text_language': self.test_ja.id,
        'translated_word': 'partial_update_translated_word',
        'translated_word_language': self.test_en.id,
    }
    dummy_phrase = PhraseFactoryWith(user=self.user,
                                     text_language=self.test_ja.id,
                                     translated_word_language=self.test_en.id)

    not_exists_url = detail_phrase_url(dummy_phrase.id) + '1'
    res = self.client.patch(not_exists_url, partial_update_payload)

    self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


def test_should_delete_phrase_with_owner(self):
    dummy_phrase = TestPhraseFactoryWith(user=self.user)
    self.assertEqual(Phrase.objects.count(), 1)
    res = self.client.delete(detail_phrase_url(dummy_phrase.id))

    self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    self.assertEqual(Phrase.objects.count(), 0)


def test_should_not_delete_phrase_with_not_owner(self):
    another_user = UserFactory(username='another_user', email='another_user@sample.com', password='another_user_pw')
    another_phrase = PhraseFactoryWith(user=another_user)
    res = self.client.delete(detail_phrase_url(another_phrase.id))

    self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
    self.assertEqual(res.data['detail'], 'You do not have permission to perform this action.')


def test_should_not_delete_phrase_with_not_exists(self):
    dummy_phrase = PhraseFactoryWith(user=self.user,
                                     text_language=self.test_ja.id,
                                     translated_word_language=self.test_en.id)
    not_exists_url = detail_phrase_url(dummy_phrase.id) + '1'
    res = self.client.delete(not_exists_url)
    self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class PhraseModelTest(TestCase):
    @freeze_time(DT)
    def setUp(self):
        self.updated_text = 'updated_text'
        self.updated_translated_word = 'updated_translated_word'
        self.updated_username = 'updated_username'

        self.user = TestUserFactory()
        self.phrase = Phrase.objects.create_phrase(user=self.user,
                                                   text='test_text',
                                                   text_language='en',
                                                   translated_word='test_translated_word',
                                                   translated_word_language='jp'
                                                   )

    def test_basic_values(self):
        self.assertEqual(self.phrase.text, 'test_text')
        self.assertEqual(self.phrase.text_language, 'en')
        self.assertEqual(self.phrase.translated_word, 'test_translated_word')
        self.assertEqual(self.phrase.translated_word_language, 'jp')
        self.assertEqual(self.phrase.created_at, DT)
        self.assertEqual(self.phrase.updated_at, DT)

    def test_value_when_edit_each_value(self):
        self.assertEqual(self.phrase.created_at, DT)
        self.assertEqual(self.phrase.updated_at, DT)

        update_time = datetime(2022, 2, 23, 2, 22)
        with freeze_time(update_time):
            self.phrase.text = self.updated_text
            self.phrase.text_language = 'jp'
            self.phrase.translated_word = self.updated_translated_word
            self.phrase.translated_word_language = 'en'
            self.user.username = self.updated_username
            self.user.save()
            self.phrase.save()

        self.assertEqual(self.phrase.text, self.updated_text)
        self.assertEqual(self.phrase.text_language, 'jp')
        self.assertEqual(self.phrase.translated_word, self.updated_translated_word)
        self.assertEqual(self.phrase.translated_word_language, 'en')
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
