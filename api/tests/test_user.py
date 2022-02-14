from django.test import TestCase
from unittest import mock
from datetime import datetime
from .factories.user import TestUserFactory
from api.models import User


class UserModelTest(TestCase):
    def setUp(self):
        self.updated_username = 'updated_username'
        self.updated_email = 'updated_email@sample.com'
        self.mock_date = datetime(2022, 2, 13, 3, 55, 18, 91811)

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = self.mock_date
            self.user = TestUserFactory()

    def test_basic_values(self):
        self.assertEqual(self.user.username, 'test_username')
        self.assertEqual(self.user.email, 'test_email@sample.com')
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.created_at, self.mock_date)
        self.assertEqual(self.user.updated_at, self.mock_date)

    def test_value_when_edit_each_value(self):
        self.user.username = self.updated_username
        self.user.email = self.updated_email
        self.user.save()
        self.assertEqual(self.user.username, self.updated_username)
        self.assertEqual(self.user.email, self.updated_email)

    def test_updated_at_when_edit_username(self):
        self.assertEqual(self.user.updated_at, self.mock_date)

        self.user.username = self.updated_username
        self.user.save()

        self.assertEqual(self.user.username, self.updated_username)
        self.assertNotEqual(self.user.updated_at.strftime("%Y-%m-%d"), '2022-02-13')

    def test_decrement_user_when_delete_user(self):
        users = User.objects.all()
        self.assertEqual(len(users), 1)
        users[0].delete()
        users = User.objects.all()
        self.assertEqual(len(users), 0)
