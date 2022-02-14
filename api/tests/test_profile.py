from django.test import TestCase
from unittest import mock
from datetime import datetime
from .factories.user import TestUserFactory
from .factories.profile import TestProfileFactoryWith
from api.models import User, Profile


class ProfileModelTest(TestCase):
    def setUp(self):
        self.updated_username = 'updated_username'
        self.mock_date = datetime(2022, 2, 13, 3, 55, 18, 91811)

        with mock.patch('django.utils.timezone.now') as mock_now:
            mock_now.return_value = self.mock_date
            self.user = TestUserFactory()
            self.profile = TestProfileFactoryWith(user=self.user)

    def test_basic_values(self):
        self.assertEqual(self.profile.user.username, 'test_username')
        self.assertEqual(self.profile.sex, 'men')
        self.assertEqual(self.profile.date_of_birth, '1993-05-01')
        self.assertEqual(self.profile.created_at, self.mock_date)
        self.assertEqual(self.profile.updated_at, self.mock_date)

    def test_username_and_updated_at_when_edit_username(self):
        self.assertEqual(self.profile.updated_at, self.mock_date)
        self.user.username = self.updated_username
        self.user.save()

        self.assertEqual(self.profile.user.username, self.updated_username)
        self.assertNotEqual(self.user.updated_at.strftime("%Y-%m-%d"), '2022-02-13')

    def test_decrement_profile_when_delete_user(self):
        users = User.objects.all()
        profiles = Profile.objects.all()

        self.assertEqual(len(users), 1)
        self.assertEqual(len(profiles), 1)

        users[0].delete()
        users = User.objects.all()
        profiles = Profile.objects.all()

        self.assertEqual(len(users), 0)
        self.assertEqual(len(profiles), 0)
