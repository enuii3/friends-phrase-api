from django.test import TestCase
from datetime import datetime
from .factories.user import TestUserFactory
from .factories.profile import TestProfileFactoryWith
from api.models import Profile
from django.contrib.auth import get_user_model
from freezegun import freeze_time

DT = datetime(2022, 2, 22, 2, 22)


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
