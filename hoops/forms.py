from django.forms import ModelForm
from .models import Attempt, Practice, BasicStats


class PracticeForm(ModelForm):
    class Meta:
        model = BasicStats
        fields = ['total_made', 'total_shots']


class EditPracticeForm(ModelForm):
    class Meta:
        model = Practice
        fields = ['date']
