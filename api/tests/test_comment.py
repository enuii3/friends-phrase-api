from django.test import TestCase
from django.urls import reverse
from datetime import datetime
from .factories.comment import TestCommentFactoryWith, CommentFactoryWith
from .factories.phrase import TestPhraseFactoryWith
from .factories.user import TestUserFactory
from api.models import Phrase, Comment
from django.contrib.auth import get_user_model
from freezegun import freeze_time
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

DT = datetime(2022, 2, 22, 2, 22)
UPDATE_DT = datetime(2022, 3, 22, 2, 22)
CREATE_COMMENT_URL = '/api/comment/'


def detail_comment_url(comment_id):
    return reverse('api:comment-detail', args=[comment_id])


class CommentApiTest(APITestCase):
    def setUp(self):
        self.user = TestUserFactory()
        self.test_phrase = TestPhraseFactoryWith(user=TestUserFactory(email='phrase_user@sample.com'))

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_should_create_comment(self):
        payload = {
            "text": 'text',
            "text_language": 'en',
            "phrase": self.test_phrase.id,
        }
        with freeze_time(DT):
            res = self.client.post(CREATE_COMMENT_URL, payload)
        comment = Comment.objects.get(**payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(comment.text, payload['text'])
        self.assertEqual(comment.text_language, payload['text_language'])
        self.assertEqual(comment.phrase, self.test_phrase)
        self.assertEqual(comment.user.username, self.user.username)
        self.assertEqual(comment.created_at, DT)
        self.assertEqual(comment.updated_at, DT)
        self.assertEqual(self.test_phrase.comments.count(), 1)

    def test_should_not_create_comment_with_blank_value(self):
        payload = {
            "text": '',
            "text_language": '',
            "phrase": '',
        }
        res = self.client.post(CREATE_COMMENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['text'][0], 'This field may not be blank.')
        self.assertEqual(res.data['text_language'][0], '"" is not a valid choice.')
        self.assertEqual(res.data['phrase'][0], 'This field may not be null.')

    def test_should_not_create_comment_with_missing_key(self):
        payload = {
            "test_text": 'text',
            "test_text_language": 'en',
            "test_phrase": self.test_phrase.id,
        }
        res = self.client.post(CREATE_COMMENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['text'][0], 'This field is required.')
        self.assertEqual(res.data['text_language'][0], 'This field is required.')
        self.assertEqual(res.data['phrase'][0], 'This field is required.')

    def test_should_update_comment(self):
        update_payload = {
            "text": 'update_text',
            "text_language": 'jp',
            "phrase": self.test_phrase.id,
        }
        with freeze_time(DT):
            dummy_comment = CommentFactoryWith(user=self.user, phrase=self.test_phrase)
        with freeze_time(UPDATE_DT):
            res = self.client.put(detail_comment_url(dummy_comment.id), update_payload)
        comment = Comment.objects.get(**update_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(comment.text, update_payload['text'])
        self.assertEqual(comment.text_language, update_payload['text_language'])
        self.assertEqual(comment.phrase, self.test_phrase)
        self.assertEqual(comment.user.username, self.user.username)
        self.assertEqual(comment.created_at, DT)
        self.assertEqual(comment.updated_at, UPDATE_DT)

    def test_should_not_update_comment_by_not_owner(self):
        update_payload = {
            "text": 'update_text',
            "text_language": 'jp',
            "phrase": self.test_phrase.id,
        }
        another_user = TestUserFactory(email='another_user@sample.com')
        another_comment = CommentFactoryWith(user=another_user, phrase=self.test_phrase, text='another_text')
        res = self.client.put(detail_comment_url(another_comment.id), update_payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['detail'], 'You do not have permission to perform this action.')

    def test_should_not_update_comment_with_blank_value(self):
        update_payload = {
            "text": '',
            "text_language": '',
            "phrase": '',
        }
        another_comment = CommentFactoryWith(phrase=self.test_phrase, user=self.user)
        res = self.client.put(detail_comment_url(another_comment.id), update_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['text'][0], 'This field may not be blank.')
        self.assertEqual(res.data['text_language'][0], '"" is not a valid choice.')
        self.assertEqual(res.data['phrase'][0], 'This field may not be null.')

    def test_should_not_update_comment_with_missing_key(self):
        update_payload = {
            "test_text": 'update_text',
            "test_text_language": 'jp',
            "test_phrase": self.test_phrase.id,
        }
        another_comment = CommentFactoryWith(text='test_text', phrase=self.test_phrase, user=self.user)
        res = self.client.put(detail_comment_url(another_comment.id), update_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['text'][0], 'This field is required.')
        self.assertEqual(res.data['text_language'][0], 'This field is required.')
        self.assertEqual(res.data['phrase'][0], 'This field is required.')

    def test_should_not_update_comment_with_not_exists(self):
        update_payload = {
            "text": 'update_text',
            "text_language": 'jp',
            "phrase": self.test_phrase.id,
        }
        another_comment = CommentFactoryWith(phrase=self.test_phrase, user=self.user)
        not_exits_comment_url = detail_comment_url(another_comment.id) + '1'
        res = self.client.put(not_exits_comment_url, update_payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_partial_update_comment(self):
        partial_update_payload = {
            "text": 'partial_update_text',
            "text_language": 'jp',
            "phrase": self.test_phrase.id,
        }
        with freeze_time(DT):
            dummy_comment = CommentFactoryWith(user=self.user, phrase=self.test_phrase)
        with freeze_time(UPDATE_DT):
            res = self.client.patch(detail_comment_url(dummy_comment.id), partial_update_payload)
        comment = Comment.objects.get(**partial_update_payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(comment.text, partial_update_payload['text'])
        self.assertEqual(comment.text_language, 'jp')
        self.assertEqual(comment.phrase, self.test_phrase)
        self.assertEqual(comment.user.username, self.user.username)
        self.assertEqual(comment.created_at, DT)
        self.assertEqual(comment.updated_at, UPDATE_DT)

    def test_should_not_partial_update_comment_by_not_owner(self):
        partial_update_payload = {
            "text": 'partial_update_text',
            "text_language": 'jp',
            "phrase": self.test_phrase.id,
        }
        another_user = TestUserFactory(email='another_user@sample.com')
        another_comment = CommentFactoryWith(user=another_user, phrase=self.test_phrase, text='another_text')
        res = self.client.patch(detail_comment_url(another_comment.id), partial_update_payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['detail'], 'You do not have permission to perform this action.')

    def test_should_not_partial_update_comment_with_blank_value(self):
        partial_update_payload = {
            "text": '',
            "text_language": '',
            "phrase": '',
        }
        comment = CommentFactoryWith(phrase=self.test_phrase, user=self.user)
        res = self.client.patch(detail_comment_url(comment.id), partial_update_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['text'][0], 'This field may not be blank.')
        self.assertEqual(res.data['text_language'][0], '"" is not a valid choice.')
        self.assertEqual(res.data['phrase'][0], 'This field may not be null.')

    def test_should_not_partial_update_comment_with_missing_key(self):
        partial_update_payload = {
            "test_text": 'partial_update_text',
            "test_text_language": 'jp',
            "test_phrase": self.test_phrase.id,
        }
        comment = CommentFactoryWith(text='test_text',
                                     text_language='en',
                                     phrase=self.test_phrase,
                                     user=self.user)
        self.client.patch(detail_comment_url(comment.id), partial_update_payload)

        self.assertEqual(comment.text, 'test_text')
        self.assertEqual(comment.text_language, 'en')
        self.assertEqual(comment.phrase, self.test_phrase)

    def test_should_not_partial_update_comment_with_not_exists(self):
        partial_update_payload = {
            "text": 'partial_update_text',
            "text_language": 'jp',
            "phrase": self.test_phrase.id,
        }
        another_comment = CommentFactoryWith(phrase=self.test_phrase, user=self.user)
        not_exits_comment_url = detail_comment_url(another_comment.id) + '1'
        res = self.client.patch(not_exits_comment_url, partial_update_payload)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_delete_comment_by_owner(self):
        comment = TestCommentFactoryWith(user=self.user, phrase=self.test_phrase)
        self.assertEqual(Comment.objects.count(), 1)
        res = self.client.delete(detail_comment_url(comment.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_should_not_delete_comment_by_not_owner(self):
        another_user = TestUserFactory(email='another_user@sample.com')
        another_comment = CommentFactoryWith(user=another_user, phrase=self.test_phrase)
        res = self.client.delete(detail_comment_url(another_comment.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['detail'], 'You do not have permission to perform this action.')

    def test_should_not_delete_with_not_exists(self):
        another_user = TestUserFactory(email='another_user@sample.com')
        another_comment = CommentFactoryWith(user=another_user, phrase=self.test_phrase, text='dummy_text')
        dummy_comment_url = detail_comment_url(another_comment.id) + '1'

        res = self.client.delete(dummy_comment_url)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class CommentModelTest(TestCase):
    @freeze_time(DT)
    def setUp(self):
        self.updated_username = 'updated_username'
        self.updated_comment_text = 'updated_comment_text'

        self.phrase_user = TestUserFactory(username='phrase_user', email='phrase_user@sample.com')
        self.comment_user = TestUserFactory(username='comment_user', email='comment_user@sample.com')
        self.phrase = TestPhraseFactoryWith(user=self.phrase_user
                                            # text_language=self.test_en,
                                            # translated_word_language=self.test_ja
                                            )
        self.payload = {'text': 'test_text', 'text_language': 'en', 'user': self.comment_user, 'phrase': self.phrase}
        self.comment = Comment.objects.create_comment(**self.payload
                                                      # text='test_text',
                                                      #                                           text_language='en',
                                                      #                                           user=self.comment_user,
                                                      #                                           phrase=self.phrase,
                                                      )

    def test_basic_values(self):
        self.assertEqual(self.comment.text, self.payload['text'])
        self.assertEqual(self.comment.text_language, self.payload['text_language'])
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
            self.comment.text_language = 'jp'
            self.comment_user.username = self.updated_username
            self.comment.save()

        self.assertEqual(self.comment.text, self.updated_comment_text)
        self.assertEqual(self.comment.text_language, 'jp')
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
