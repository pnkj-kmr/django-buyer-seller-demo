from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    CHOICES = (('Buyer', 'Buyer'),('Seller', 'Seller'),)
    first_name = forms.ChoiceField(label="User Type", choices=CHOICES)
    username = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2')
