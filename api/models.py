from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import uuid

language_max_length = 3


class UserManager(BaseUserManager):
    def create_user(self, username, email, password):
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
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
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
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    sex = models.CharField(max_length=7, choices=SEX_CHOICES)
    date_of_birth = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def __str__(self):
        return str(self.user)


class Language(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('ja', 'Japanese'),
    )

    name = models.CharField(max_length=language_max_length, choices=LANGUAGE_CHOICES)

    objects = models.Manager()

    def __str__(self):
        return self.name


class PhraseManager(models.Manager):
    def create_phrase(self, text, text_language, translated_word, translated_word_language, user):
        if not text:
            raise ValueError('text is must')
        if not text_language:
            raise ValueError('text_language is must')
        if not translated_word:
            raise ValueError('translated_word is must')
        if not translated_word_language:
            raise ValueError('translated_word_language is must')
        if not user:
            raise ValueError('user is must')

        phrase = self.create(text=text, translated_word=translated_word, user=user)
        phrase.text_language.add(text_language)
        phrase.translated_word_language.add(translated_word_language)
        phrase.save()
        return phrase


class Phrase(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
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

    objects = PhraseManager()

    def __str__(self):
        return self.text


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
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
