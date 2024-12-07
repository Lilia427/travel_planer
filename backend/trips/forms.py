from django import forms
from django.contrib.auth.models import User
from .models import Order

# Форма реєстрації
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', 'Паролі не збігаються.')

# Форма входу
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# Форма вибору міста та дати
class TravelForm(forms.Form):
    CITY_CHOICES = [
        ('lviv', 'Львів'),
        ('kyiv', 'Київ'),
        ('odesa', 'Одеса'),
        ('dnieper', 'Дніпро'),
        ('vinnytsia', 'Вінниця'),
        ('uzhhorod', 'Ужгород'),
        ('chernivtsi', 'Чернівці'),
        ('ivano-frankivsk', 'Івано-Франківськ'),
        ('lutsk', 'Луцьк'),
        ('khmelnytskyi', 'Хмельницький'),
        ('ternopil', 'Тернопіль'),
        ('poltava', 'Полтава'),
        ('chernihiv', 'Чернігів'),
        ('rivno', 'Рівне'),
        ('zhytomyr', 'Житомир'),
    ]
    city = forms.ChoiceField(choices=CITY_CHOICES, label="Місто")
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Дата початку")
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label="Дата завершення")
