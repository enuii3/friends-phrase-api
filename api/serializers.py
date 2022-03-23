from rest_framework import serializers

from .models import Profile, Language, Phrase
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


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Profile
        fields = ['id', 'sex', 'date_of_birth', 'created_at', 'updated_at', 'username']
        extra_kwargs = {
            'sex': {'required': True},
            'date_of_birth': {'required': True},
        }


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class PhraseSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

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
                  ]

        extra_kwargs = {
            'text': {'required': True},
            'text_language': {'required': True},
            'translated_word': {'required': True},
            'translated_word_language': {'required': True},
        }
