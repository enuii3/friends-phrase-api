from django.test import TestCase
from datetime import datetime
from .factories.user import TestUserFactory
from django.contrib.auth import get_user_model
from freezegun import freeze_time

DT = datetime(2022, 2, 22, 2, 22)


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
