from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)
from django.core.exceptions import ValidationError
from django.shortcuts import redirect

from app_channel.models import Channel
from .models import User


class LoginForm(AuthenticationForm):
    """Форма для логина пользователя"""

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')

    def is_valid(self):
        email = self.data.get('email')
        password = self.data.get('password')
        user = authenticate(self.request, email=email, password=password)
        if user:
            login(self.request, user)
            return redirect('index')


class RegistrationForm(UserCreationForm):
    """Форма для регистрации пользователя"""

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        """Проверка на уникальность поля email по БД"""

        email = self.cleaned_data['email']
        records = User.objects.filter(email=email)
        if records:
            raise ValidationError('Пользователь с таким email уже существует')
        return email

    def save(self, commit=True):
        """При регистрации польщователя создаем ему сразу канал с дефолтными данными"""

        result = super().save(commit=True)
        user = User.objects.filter(email=self.cleaned_data.get('email')).first()
        Channel.objects.create(
            channel_name=self.cleaned_data.get('username'),
            full_name=self.cleaned_data.get('username'),
            description=self.cleaned_data.get('username'),
            owner=user,

        )

        return result