from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('login_user/', views.RetrieveLonginUserView.as_view(), name='login_user'),
    path('user/', views.CreateUserView.as_view(), name='create_user'),
    path('user/<uuid:pk>/', views.RetrieveUpdateDestroyUserView.as_view(), name='user'),
]
