from rest_framework import serializers

from .models import Profile, Phrase, Comment
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'created_at', 'updated_at']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'password': {'write_only': True, 'required': True, 'min_length': 8},
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username']
        extra_kwargs = {
            'username': {'required': True},
        }


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ['id', 'sex', 'date_of_birth', 'created_at', 'updated_at', 'username']
        extra_kwargs = {
            'sex': {'required': True},
            'date_of_birth': {'required': True},
        }


class PhraseSerializer(serializers.ModelSerializer):
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('jp', 'Japanese'),
    )
    username = serializers.ReadOnlyField(source='user.username')
    text_language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)
    translated_word_language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)

    class Meta:
        model = Phrase
        fields = ['id',
                  'text',
                  'text_language',
                  'translated_word',
                  'translated_word_language',
                  'created_at',
                  'updated_at',
                  'username',
                  'comments',
                  ]

        extra_kwargs = {
            'text': {'required': True},
            'text_language': {'required': True},
            'translated_word': {'required': True},
            'translated_word_language': {'required': True},
            'comments': {'read_only': True}
        }


class CommentSerializer(serializers.ModelSerializer):
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('jp', 'Japanese'),
    )
    username = serializers.ReadOnlyField(source='user.username')
    text_language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)
    phrase = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Phrase.objects.all()
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'text_language', 'created_at', 'updated_at', 'username', 'phrase']
        extra_kwargs = {
            'text': {'required': True},
            'text_language': {'required': True},
        }
