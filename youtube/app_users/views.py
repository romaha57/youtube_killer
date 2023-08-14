from app_users.forms import LoginForm, RegistrationForm
from app_users.models import User
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView


class UserLoginView(LoginView):
    """Логин пользователя"""

    form_class = LoginForm
    template_name = 'userauths/sign-in.html'


class UserRegistrationView(SuccessMessageMixin, CreateView):
    """Регистрация пользователя"""

    model = User
    form_class = RegistrationForm
    template_name = 'userauths/sign-up.html'
    success_url = reverse_lazy('sign-in')
    success_message = 'Вы успешно зарегистрировались'
