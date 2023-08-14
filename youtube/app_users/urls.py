from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import UserLoginView, UserRegistrationView

urlpatterns = [
    path('sign-in/', UserLoginView.as_view(), name='sign-in'),
    path('sign-up/', UserRegistrationView.as_view(), name='sign-up'),
    path('sign-out/', LogoutView.as_view(), name='sign-out'),
]
