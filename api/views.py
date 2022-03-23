from rest_framework import generics, permissions, viewsets
from .serializers import UserSerializer, ProfileSerializer, LanguageSerializer
from .models import User, Profile, Language
from .permissions import IsOwnerOrReadOnly


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class RetrieveLonginUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class RetrieveUpdateDestroyUserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetrieveLanguage(generics.RetrieveAPIView):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
