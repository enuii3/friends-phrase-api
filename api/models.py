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
    icon = models.ImageField(upload_to='icons', verbose_name='アイコン', default='icons/default.png')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

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

        phrase = self.create(text=text, text_language=text_language, translated_word=translated_word,
                             translated_word_language=translated_word_language,
                             user=user)
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
    text_language = models.CharField(max_length=8)
    translated_word = models.CharField(
        max_length=1000,
    )
    translated_word_language = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PhraseManager()

    def __str__(self):
        return self.text


class CommentManager(models.Manager):
    def create_comment(self, text, text_language, user, phrase):
        if not text:
            raise ValueError('text is must')
        if not text_language:
            raise ValueError('text_language is must')
        if not phrase:
            raise ValueError('phrase is must')
        if not user:
            raise ValueError('user is must')

        comment = self.create(text=text, text_language=text_language, user=user, phrase=phrase)
        comment.save()
        return comment


class Comment(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    text = models.CharField(max_length=1000)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE, related_name='comments')
    text_language = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CommentManager()

    def __str__(self):
        return self.text
