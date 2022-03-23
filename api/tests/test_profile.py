from datetime import datetime
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .factories.user import TestUserFactory
from .factories.profile import TestProfileFactoryWith
from api.models import Profile
from django.contrib.auth import get_user_model
from freezegun import freeze_time
from django.db import IntegrityError

DT = datetime(2022, 2, 22, 2, 22)
UPDATE_DT = datetime(2022, 3, 22, 2, 22)
CREATE_PROFILE_URL = '/api/profile/'
LOGIN_URL = '/api/login_user/'


def detail_profile_url(profile_id):
    return reverse('api:profile-detail', args=[profile_id])


class ProfileApiTest(TestCase):
    def setUp(self):
        self.user = TestUserFactory()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_should_create_profile(self):
        payload = {'sex': 'men', 'date_of_birth': '1993-05-01'}
        with freeze_time(DT):
            res = self.client.post(CREATE_PROFILE_URL, payload)
        profile = Profile.objects.get(id=res.data['id'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(profile.sex, payload['sex'])
        self.assertEqual(profile.date_of_birth, payload['date_of_birth'])
        self.assertEqual(profile.user.username, self.user.username)
        self.assertEqual(profile.created_at, DT)
        self.assertEqual(profile.updated_at, DT)

    def test_should_not_create_profile_when_already_exits(self):
        payload = {'sex': 'men', 'date_of_birth': '1993-05-01'}
        self.client.post(CREATE_PROFILE_URL, payload)

        with self.assertRaises(IntegrityError):
            self.client.post(CREATE_PROFILE_URL, payload)

    def test_should_not_create_profile_when_blank_value(self):
        missing_payload = {'sex': '', 'date_of_birth': ''}
        res = self.client.post(CREATE_PROFILE_URL, missing_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['sex'][0], '"" is not a valid choice.')
        self.assertEqual(res.data['date_of_birth'][0], 'This field may not be blank.')

    def test_should_not_create_profile_when_missing_key(self):
        missing_payload = {'test_sex': 'men', 'test_date_of_birth': '1993-05-01'}
        res = self.client.post(CREATE_PROFILE_URL, missing_payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['sex'][0], 'This field is required.')
        self.assertEqual(res.data['date_of_birth'][0], 'This field is required.')

    def test_should_update_profile_with_owner(self):
        payload = {'sex': 'men', 'date_of_birth': '1993-05-01'}
        with freeze_time(DT):
            res = self.client.post(CREATE_PROFILE_URL, payload)
        profile = Profile.objects.get(id=res.data['id'])

        self.assertEqual(profile.created_at, DT)
        self.assertEqual(profile.updated_at, DT)

        payload['date_of_birth'] = '1994-05-01'
        with freeze_time(UPDATE_DT):
            updated_res = self.client.put(detail_profile_url(profile.id), payload)
        profile.refresh_from_db()

        self.assertEqual(updated_res.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.date_of_birth, payload['date_of_birth'])
        self.assertEqual(profile.created_at, DT)
        self.assertEqual(profile.updated_at, UPDATE_DT)

    def test_should_not_update_profile_with_not_owner(self):
        another_user = TestUserFactory(username='another_user', email='another_user@sample.com')
        another_user_profile = TestProfileFactoryWith(user=another_user)
        payload = {'sex': 'men', 'date_of_birth': '1993-05-01'}
        self.client.post(CREATE_PROFILE_URL, payload)
        payload['date_of_birth'] = '1994-05-01'
        res = self.client.put(detail_profile_url(another_user_profile.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['detail'], 'You do not have permission to perform this action.')

    def test_should_not_update_profile_with_blank_value(self):
        payload = {'sex': 'men', 'date_of_birth': '1993-05-01'}
        res = self.client.post(CREATE_PROFILE_URL, payload)
        missing_payload = {'sex': '', 'date_of_birth': ''}
        updated_res = self.client.put(detail_profile_url(res.data['id']), missing_payload)

        self.assertEqual(updated_res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(updated_res.data['sex'][0], '"" is not a valid choice.')
        self.assertEqual(updated_res.data['date_of_birth'][0], 'This field may not be blank.')

    def test_should_not_update_profile_with_missing_key(self):
        payload = {'sex': 'men', 'date_of_birth': '1993-05-01'}
        res = self.client.post(CREATE_PROFILE_URL, payload)
        missing_payload = {'test_sex': 'men', 'test_date_of_birth': '1993-05-01'}
        updated_res = self.client.put(detail_profile_url(res.data['id']), missing_payload)

        self.assertEqual(updated_res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(updated_res.data['sex'][0], 'This field is required.')
        self.assertEqual(updated_res.data['date_of_birth'][0], 'This field is required.')

    def test_should_not_update_profile_when_not_exits(self):
        payload = {'sex': 'men', 'date_of_birth': '1993-05-01'}
        res = self.client.put(CREATE_PROFILE_URL + "id/", payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.data['detail'], 'Not found.')

    def test_should_partial_update_profile_with_owner(self):
        payload = {'sex': 'men', 'date_of_birth': '1993-05-01'}
        with freeze_time(DT):
            res = self.client.post(CREATE_PROFILE_URL, payload)
        profile = Profile.objects.get(id=res.data['id'])

        self.assertEqual(profile.created_at, DT)
        self.assertEqual(profile.updated_at, DT)

        payload['date_of_birth'] = '1994-05-01'
        with freeze_time(UPDATE_DT):
            partial_updated_res = self.client.patch(detail_profile_url(profile.id), payload)
        profile.refresh_from_db()

        self.assertEqual(partial_updated_res.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.date_of_birth, payload['date_of_birth'])
        self.assertEqual(profile.created_at, DT)
        self.assertEqual(profile.updated_at, UPDATE_DT)

    def test_should_not_partial_update_profile_with_not_owner(self):
        another_user = TestUserFactory(username='another_user', email='another_user@sample.com')
        another_user_profile = TestProfileFactoryWith(user=another_user)
        payload = {'sex': 'men', 'date_of_birth': '1993-05-01'}
        self.client.post(CREATE_PROFILE_URL, payload)
        payload['date_of_birth'] = '1994-05-01'
        res = self.client.patch(detail_profile_url(another_user_profile.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['detail'], 'You do not have permission to perform this action.')

    def test_should_not_partial_update_profile_with_blank_value(self):
        payload = {'sex': 'men', 'date_of_birth': '1993-05-01'}
        res = self.client.post(CREATE_PROFILE_URL, payload)
        missing_payload = {'sex': '', 'date_of_birth': ''}
        partial_updated_res = self.client.patch(detail_profile_url(res.data['id']), missing_payload)

        self.assertEqual(partial_updated_res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(partial_updated_res.data['sex'][0], '"" is not a valid choice.')
        self.assertEqual(partial_updated_res.data['date_of_birth'][0], 'This field may not be blank.')

    def test_should_not_partial_update_profile_with_missing_key(self):
        payload = {'sex': 'men', 'date_of_birth': '1993-05-01'}
        missing_payload = {'test_sex': 'women', 'test_date_of_birth': '1994-05-01'}
        res = self.client.post(CREATE_PROFILE_URL, payload)
        profile = Profile.objects.get(id=res.data['id'])
        self.client.patch(detail_profile_url(profile.id), missing_payload)
        profile.refresh_from_db()

        self.assertEqual(profile.sex, payload['sex'])
        self.assertEqual(profile.date_of_birth, payload['date_of_birth'])

    def test_should_not_partial_update_profile_when_not_exits(self):
        payload = {'sex': 'men', 'date_of_birth': '1993-05-01'}
        res = self.client.patch(CREATE_PROFILE_URL + "id/", payload)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.data['detail'], 'Not found.')

    def test_should_delete_profile_with_owner(self):
        payload = {'sex': 'men', 'date_of_birth': '1993-05-01'}
        profile = self.client.post(CREATE_PROFILE_URL, payload)
        self.assertEqual(Profile.objects.count(), 1)
        res = self.client.delete(detail_profile_url(profile.data['id']))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Profile.objects.count(), 0)

    def test_should_not_delete_profile_with_not_owner(self):
        another_user = TestUserFactory(username='another_user', email='another_user@sample.com')
        another_user_profile = TestProfileFactoryWith(user=another_user)
        res = self.client.delete(detail_profile_url(another_user_profile.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['detail'], 'You do not have permission to perform this action.')

    def test_should_not_delete_profile_by_not_exists(self):
        res = self.client.delete(CREATE_PROFILE_URL + "nothing_id/")

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.data['detail'], 'Not found.')


class ProfileModelTest(TestCase):

    @freeze_time(DT)
    def setUp(self):
        self.updated_username = 'updated_username'
        self.fix_sex = 'woman'
        self.fix_date_of_birth = '2000-05-01'
        self.user = TestUserFactory()
        self.profile = TestProfileFactoryWith(user=self.user)

    def test_basic_values(self):
        self.assertEqual(self.profile.user.username, 'test_username')
        self.assertEqual(self.profile.sex, 'men')
        self.assertEqual(self.profile.date_of_birth, '1993-05-01')
        self.assertEqual(self.profile.created_at, DT)
        self.assertEqual(self.profile.updated_at, DT)

    def test_value_when_edit_each_value(self):
        self.assertEqual(self.profile.created_at, DT)
        self.assertEqual(self.profile.updated_at, DT)

        update_time = datetime(2022, 2, 23, 2, 22)
        with freeze_time(update_time):
            self.user.username = self.updated_username
            self.profile.sex = self.fix_sex
            self.profile.date_of_birth = self.fix_date_of_birth
            self.user.save()
            self.profile.save()

        self.assertEqual(self.profile.user.username, self.updated_username)
        self.assertEqual(self.profile.sex, self.fix_sex)
        self.assertEqual(self.profile.date_of_birth, self.fix_date_of_birth)
        self.assertEqual(self.profile.created_at, DT)
        self.assertEqual(self.profile.updated_at, update_time)

    def test_decrement_profile_when_delete_user(self):
        user_count = get_user_model().objects.count()
        profile_count = Profile.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(profile_count, 1)

        get_user_model().objects.first().delete()

        user_count = get_user_model().objects.count()
        profile_count = Profile.objects.count()

        self.assertEqual(user_count, 0)
        self.assertEqual(profile_count, 0)

    def test_decrement_profile_when_delete_profile(self):
        user_count = get_user_model().objects.count()
        profile_count = Profile.objects.count()
        self.assertEqual(user_count, 1)
        self.assertEqual(profile_count, 1)

        Profile.objects.first().delete()

        user_count = get_user_model().objects.count()
        profile_count = Profile.objects.count()

        self.assertEqual(user_count, 1)
        self.assertEqual(profile_count, 0)
