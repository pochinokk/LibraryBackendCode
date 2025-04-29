from django import forms
from .models import CustomUser, Book
from django.contrib.auth.forms import UserCreationForm


class CustomLoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(label='ФИО', max_length=255, required=True)
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Необязательное поле'
        })
    )
    address = forms.CharField(
        label='Адрес',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Необязательное поле'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'password1', 'password2', 'phone', 'address']

class CustomUserEditForm(forms.ModelForm):
    full_name = forms.CharField(label='ФИО', max_length=255, required=True)
    phone = forms.CharField(
        label='Телефон',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Необязательное поле'
        })
    )
    address = forms.CharField(
        label='Адрес',
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Необязательное поле'
        })
    )
    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'phone', 'address']


class BookForm(forms.ModelForm):
    printing_year = forms.IntegerField(
        required=False,
        min_value=0
    )
    class Meta:
        model = Book
        fields = ('name', 'author', 'printing_year', 'language', 'end_date', 'is_taken', 'reader')
        widgets = {
            'name': forms.TextInput(attrs={'maxlength': 255}),
            'author': forms.TextInput(attrs={'maxlength': 255}),
            'language': forms.TextInput(attrs={'maxlength': 100}),
            # 'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
