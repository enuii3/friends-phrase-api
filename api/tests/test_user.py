from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from freezegun import freeze_time
from .factories.user import TestUserFactory

DT = datetime(2022, 2, 22, 2, 22)
UPDATE_DT = datetime(2022, 3, 22, 2, 22)
CREATE_USER_URL = '/api/users/'
LOGIN_USER_URL = '/api/login_user/'
TOKEN_URL = '/authen/jwt/create/'


def detail_user_url(user_id):
    return reverse('api:user', args=[user_id])


class AuthorizedUserApiTest(TestCase):
    def setUp(self):
        with freeze_time(DT):
            self.user = TestUserFactory(password='dummy_pw')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_should_return_login_user(self):
        res = self.client.get(LOGIN_USER_URL)

        self.assertEqual(res.data['username'], self.user.username)

    def test_should_partial_update_user(self):
        payload = {'username': 'update_username', 'email': 'update_username@sample.com', 'password': 'dummy_pw'}
        with freeze_time(UPDATE_DT):
            res = self.client.patch(detail_user_url(self.user.id), payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, payload['username'])
        self.assertEqual(self.user.email, payload['email'])
        self.assertEqual(self.user.created_at, DT)
        self.assertEqual(self.user.updated_at, UPDATE_DT)

    def test_should_not_partial_update_when_missing_key(self):
        payload = {'update_username': 'update_username',
                   'update_email': 'update_email@sample.com',
                   'update_password': 'update_dummy_pw'}
        res = self.client.patch(detail_user_url(self.user.id), payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.user.username, payload['update_username'])
        self.assertNotEqual(self.user.email, payload['update_email'])
        self.assertNotEqual(self.user.password, payload['update_password'])

    def test_should_not_partial_update_when_blank_value(self):
        payload = {'username': '', 'email': '', 'password': ''}
        res = self.client.patch(detail_user_url(self.user.id), payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['username'][0], 'This field may not be blank.')
        self.assertEqual(res.data['email'][0], 'This field may not be blank.')
        self.assertEqual(res.data['password'][0], 'This field may not be blank.')

    def test_should_not_partial_update_when_not_exits(self):
        payload = {'username': 'update_username', 'email': 'update_username@sample.com', 'password': 'dummy_pw'}
        dummy_url = detail_user_url(self.user.id) + '1'
        res = self.client.patch(dummy_url, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_not_partial_update_user_when_not_owner(self):
        payload = {'username': 'update_username', 'email': 'update_email@sample.com', 'password': 'update_password'}
        another_user = TestUserFactory(email='another_email@sample.com')
        res = self.client.patch(detail_user_url(another_user.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['detail'], 'You do not have permission to perform this action.')

    def test_should_update_user(self):
        payload = {'username': 'update_username', 'email': 'update_username@sample.com', 'password': 'dummy_pw'}
        res = self.client.put(detail_user_url(self.user.id), payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.username, payload['username'])
        self.assertEqual(self.user.email, payload['email'])

    def test_should_not_update_user_with_blank_value(self):
        payload = {'username': '', 'email': '', 'password': ''}
        res = self.client.put(detail_user_url(self.user.id), payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['username'][0], 'This field may not be blank.')
        self.assertEqual(res.data['email'][0], 'This field may not be blank.')
        self.assertEqual(res.data['password'][0], 'This field may not be blank.')

    def test_should_not_update_user_with_missing_key(self):
        payload = {'update_username': 'update_username',
                   'update_email': 'update_email@sample.com',
                   'update_password': 'update_dummy_pw'}

        res = self.client.put(detail_user_url(self.user.id), payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['username'][0], 'This field is required.')
        self.assertEqual(res.data['email'][0], 'This field is required.')
        self.assertEqual(res.data['password'][0], 'This field is required.')

    def test_should_not_update_user_with_not_exits(self):
        payload = {'username': 'update_username', 'email': 'update_username@sample.com', 'password': 'dummy_pw'}
        dummy_url = detail_user_url(self.user.id) + '1'
        with freeze_time(UPDATE_DT):
            res = self.client.put(dummy_url, payload)
        self.user.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_should_not_update_user_by_not_owner(self):
        payload = {'username': 'update_username', 'email': 'update_email@sample.com', 'password': 'update_password'}
        another_user = TestUserFactory(email='another_email@sample.com')
        res = self.client.put(detail_user_url(another_user.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['detail'], 'You do not have permission to perform this action.')

    def test_should_delete_user(self):
        self.assertEqual(get_user_model().objects.count(), 1)
        res = self.client.delete(detail_user_url(self.user.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(get_user_model().objects.count(), 0)

    def test_should_not_delete_user_by_not_owner(self):
        another_user = TestUserFactory(email='another_email@sample.com')
        res = self.client.delete(detail_user_url(another_user.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.data['detail'], 'You do not have permission to perform this action.')

    def test_should_not_delete_user_with_not_exits(self):
        another_user = TestUserFactory(email='another_email@sample.com')
        dummy_url = detail_user_url(another_user.id) + '1'
        res = self.client.delete(dummy_url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class UnAuthorizedUserApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_should_return_access_token(self):
        payload = {'username': 'test_user', 'email': 'test_user@sample.com', 'password': 'dummy_pw'}
        get_user_model().objects.create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_should_not_return_access_token_when_blank_value(self):
        payload = {'username': '', 'email': '', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.data['email'][0], 'This field may not be blank.')
        self.assertEqual(res.data['password'][0], 'This field may not be blank.')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_not_return_access_token_when_missing_key(self):
        payload = {'test_username': 'test_user', 'test_email': 'test_user@sample.com', 'test_password': 'dummy_pw'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.data['email'][0], 'This field is required.')
        self.assertEqual(res.data['password'][0], 'This field is required.')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_should_return_401_response_by_un_authorized_user(self):
        res = self.client.get(LOGIN_USER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data['detail'], 'Authentication credentials were not provided.')

    def test_should_create_new_user(self):
        payload = {'username': 'dummy', 'email': 'dummy@sample.com', 'password': 'dummy_pw'}
        with freeze_time(DT):
            res = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(**res.data)

        self.assertEqual(get_user_model().objects.count(), 1)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.username, payload['username'])
        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        self.assertEqual(user.created_at, DT)
        self.assertEqual(user.updated_at, DT)

    def test_should_not_create_user_by_some_credential(self):
        payload = {'username': 'dummy', 'email': 'dummy@sample.com', 'password': 'dummy_pw'}
        get_user_model().objects.create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['email'][0], 'user with this email already exists.')

    def test_should_not_create_user_by_short_password(self):
        payload = {'username': 'dummy', 'email': 'dummy@sample.com', 'password': 'dummy'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['password'][0], 'Ensure this field has at least 8 characters.')

    def test_should_not_create_user_by_blank_value(self):
        payload = {'username': '', 'email': '', 'password': ''}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['username'][0], 'This field may not be blank.')
        self.assertEqual(res.data['email'][0], 'This field may not be blank.')
        self.assertEqual(res.data['password'][0], 'This field may not be blank.')

    def test_should_not_create_user_by_missing_key(self):
        payload = {'test_username': 'dummy', 'test_email': 'dummy@sample.com', 'test_password': 'dummy_pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.data['username'][0], 'This field is required.')
        self.assertEqual(res.data['email'][0], 'This field is required.')
        self.assertEqual(res.data['password'][0], 'This field is required.')

    def test_should_response_token_with_valid(self):
        payload = {'username': 'dummy', 'email': 'dummy@sample.com', 'password': 'dummy_pw'}
        get_user_model().objects.create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_should_not_response_token_with_invalid_credential(self):
        get_user_model().objects.create_user(username='dummy', email='dummy@sample.com', password='dummy_pw')
        invalid_payload = {'username': 'dummy', 'email': 'dummy@sample.com', 'password': 'dummy_dummy'}
        res = self.client.post(TOKEN_URL, invalid_payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data['detail'], 'No active account found with the given credentials')

    def test_should_not_response_token_with_non_exist_credential(self):
        payload = {'username': 'dummy', 'email': 'dummy@sample.com', 'password': 'dummy_pw'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data['detail'], 'No active account found with the given credentials')

    def test_should_not_response_token_with_missing_field(self):
        missing_payload = {'user': 'dummy', 'email': 'dummy@sample.com', 'password': 'dummy_dummy'}
        res = self.client.post(TOKEN_URL, missing_payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.data['detail'], 'No active account found with the given credentials')


class UserModelTest(TestCase):

    @freeze_time(DT)
    def setUp(self):
        self.updated_username = 'updated_username'
        self.updated_email = 'updated_email@sample.com'
        self.user = TestUserFactory()

    def test_basic_values(self):
        self.assertEqual(self.user.username, 'test_username')
        self.assertEqual(self.user.email, 'test_email@sample.com')
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.created_at, DT)
        self.assertEqual(self.user.updated_at, DT)

    def test_value_when_edit_each_value(self):
        self.assertEqual(self.user.created_at, DT)
        self.assertEqual(self.user.updated_at, DT)

        update_time = datetime(2022, 2, 23, 2, 22)
        with freeze_time(update_time):
            self.user.username = self.updated_username
            self.user.email = self.updated_email
            self.user.save()

        self.assertEqual(self.user.username, self.updated_username)
        self.assertEqual(self.user.email, self.updated_email)
        self.assertEqual(self.user.created_at, DT)
        self.assertEqual(self.user.updated_at, update_time)

    def test_decrement_user_when_delete_user(self):
        user_count = get_user_model().objects.count()
        self.assertEqual(user_count, 1)

        get_user_model().objects.first().delete()

        user_count = get_user_model().objects.count()
        self.assertEqual(user_count, 0)
