from rest_framework import serializers
from .models import Profile, Phrase, Comment
from django.contrib.auth import get_user_model


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'icon']
        extra_kwargs = {
            'username': {'read_only': True},
            'icon': {'read_only': True}
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


class PostUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'icon']

    extra_kwargs = {
        'username': {'read_only': True},
        'icon': {'read_only': True},
    }


class PhraseSerializer(serializers.ModelSerializer):
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('jp', 'Japanese'),
    )
    user = PostUserSerializer(read_only=True)
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
                  'user',
                  'comments',
                  ]

        extra_kwargs = {
            'text': {'required': True},
            'text_language': {'required': True},
            'translated_word': {'required': True},
            'translated_word_language': {'required': True},
            'comments': {'read_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    phrases = PhraseSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'icon', 'phrases']
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True},
            'password': {'write_only': True, 'required': True, 'min_length': 8},
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('jp', 'Japanese'),
    )
    user = PostUserSerializer(read_only=True)
    text_language = serializers.ChoiceField(choices=LANGUAGE_CHOICES)
    phrase = serializers.PrimaryKeyRelatedField(
        many=False,
        queryset=Phrase.objects.all()
    )

    class Meta:
        model = Comment
        fields = ['id', 'text', 'text_language', 'created_at', 'updated_at', 'user', 'phrase']
        extra_kwargs = {
            'text': {'required': True},
            'text_language': {'required': True},
        }
