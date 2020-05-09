from django.forms import ModelForm
from .models import Attempt, Practice, BasicStats, MyUser
from django.contrib.auth.forms import UserChangeForm


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


class EditUserForm(UserChangeForm):
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'location']
