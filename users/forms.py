from django.forms import ModelForm
from . models import Profile
from django.contrib.auth.models import User


class LoginForm(ModelForm):
    class Meta: 
        model = User
        fields = ['username', 'password']