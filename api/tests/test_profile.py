from django.test import TestCase
from unittest import mock
from datetime import datetime
from .factories.user import TestUserFactory
from .factories.profile import TestProfileFactoryWith
from api.models import Profile
from django.contrib.auth import get_user_model


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
        self.assertEqual(self.profile.created_at, self.mock_date)
        self.assertEqual(self.profile.updated_at, self.mock_date)

        self.user.username = self.updated_username
        self.user.save()

        self.assertEqual(self.profile.user.username, self.updated_username)
        self.assertEqual(self.user.created_at.strftime("%Y-%m-%d"), '2022-02-13')
        self.assertNotEqual(self.user.updated_at.strftime("%Y-%m-%d"), '2022-02-13')

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
