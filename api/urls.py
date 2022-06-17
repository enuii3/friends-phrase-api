from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('profiles', views.ProfileViewSet)
router.register('phrases', views.PhraseViewSet)
router.register('comments', views.CommentViewSet)

app_name = 'api'

urlpatterns = [
    path('login_user/', views.RetrieveLoginUserView.as_view(), name='login_user'),
    path('users/', views.CreateUserView.as_view(), name='create_user'),
    path('users/<uuid:pk>/', views.RetrieveUpdateDestroyUserView.as_view(), name='user'),
    path('', include(router.urls)),
]
