# -*- coding: utf-8 -*-
from django import forms
from django.utils import timezone
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = (self.cleaned_data['username']).lower()
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Неверное имя пользователя или пароль!')
        user = User.objects.get(username=username)
        if user and not user.check_password(password):
            raise forms.ValidationError('Неверное имя пользователя или пароль!')


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_check = forms.CharField(widget=forms.PasswordInput)
    email = forms.CharField(widget=forms.EmailInput)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password_check',
            'first_name',
            'last_name',
            'email'
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['password'].help_text = 'Придумайте пароль'
        self.fields['password_check'].label = 'Повторите пароль'
        self.fields['email'].label = 'Ваша почта'
        self.fields['email'].help_text = 'Пожалуйста, указывайте реальный адрес'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'


    def clean(self):
        username = (self.cleaned_data['username']).lower()
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        email = self.cleaned_data['email']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с данным логином уже зарегистрирован в системе!')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с данным почтовым адресом уже зарегистрирован!')
        if password != password_check:
            raise forms.ValidationError('Ваши пароли не совпадают! Попробуйте снова!')


class OrderForm(forms.Form):
    name = forms.CharField()
    last_name = forms.CharField(required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '+375 (29) 123-45-67'}))
    address = forms.CharField(required=False)
    buying_type = forms.ChoiceField(widget=forms.Select(),
                                    choices=([('Самовывоз', 'Самовывоз'), ('Доставка курьером', 'Доставка')]))
    date = forms.DateField(widget=forms.SelectDateWidget(), initial=timezone.now())
    comments = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'
        self.fields['phone'].label = 'Контактный телефон'
        self.fields[
            'phone'].help_text = 'Пожалуйста, указывате реальный номер телефона, по которому с Вами можно связаться'
        self.fields['buying_type'].label = 'Способ получения'
        self.fields['address'].label = 'Адрес доставки'
        self.fields['address'].help_text = 'Обязательно указывайте город'
        self.fields['comments'].label = 'Комментарий к заказу'
        self.fields['date'].label = 'Дата самовывоза/доставки'
        self.fields[
            'date'].help_text = 'Доставка производится на следующий день после оформления заказа. Наш менеджер свжется с Вами.'


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    phone = forms.CharField(max_length=19, min_length=19)
    message = forms.CharField(max_length=500)
