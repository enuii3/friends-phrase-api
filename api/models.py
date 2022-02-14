from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,  PermissionsMixin
from django.conf import settings

language_max_length = 3


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('email is must')

        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "username"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


class Profile(models.Model):
    SEX_CHOICES = (
        ('men', 'men'),
        ('women', 'women'),
        ('another', 'another'),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    sex = models.CharField(max_length=7, choices=SEX_CHOICES)
    date_of_birth = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.user)


class Language(models.Model):
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('ja', 'Japanese'),
    )

    name = models.CharField(max_length=language_max_length, choices=LANGUAGE_CHOICES)

    def __str__(self):
        return self.name


class Phrase(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    text = models.CharField(
        max_length=1000
    )
    text_language = models.ManyToManyField(
        Language,
        related_name='text_language',
    )
    translated_word = models.CharField(
        max_length=1000,
    )
    translated_word_language = models.ManyToManyField(
        Language,
        related_name='translated_word_language',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.text


class Comment(models.Model):
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
    text_language = models.ManyToManyField(
        Language,
        related_name='comment_language'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return self.text
