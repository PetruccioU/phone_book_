from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *


# Форма для создания обьекта модели.
class AddPersonCardForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Тип регистрации не выбран'

    class Meta:
        model = PhoneCard
        fields = ['phone_number',
                  'slug',
                  'name',
                  'company_division_name',
                  'is_published',
                  'address',
                  'cat']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите номер телефона...'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите слаг...'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите ФИО физического лица...'
            }),
            'company_division_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите название подразделения...'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите адрес организации...'
            }),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(phone_number) > 30:
            raise ValidationError('Номер телефона длиннее 12 символов!')
        return phone_number


# Форма регистрации.
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Ввидите логин пользователя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Введите Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Введите пароль еще раз',
                                widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


# Форма для логина.
class LoginUserForm(AuthenticationForm):
   username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
   password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))



