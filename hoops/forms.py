from django.forms import ModelForm
from .models import Attempt, Practice, BasicStats
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User


class PracticeForm(ModelForm):
    class Meta:
        model = BasicStats
        fields = ['total_made', 'total_shots']


class EditPracticeForm(ModelForm):
    class Meta:
        model = Practice
        fields = ['date']


class EditAttemptForm(ModelForm):
    class Meta:
        model = Attempt
        fields = ['attempts_successful', 'attempts']


class EditUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']
