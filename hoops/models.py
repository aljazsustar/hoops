from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Practice(models.Model):
    date = models.DateField(default=timezone.now().date())
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Attempt(models.Model):
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    attempts_successful = models.PositiveSmallIntegerField()
    attempts = models.PositiveSmallIntegerField()


class BasicStats(models.Model):
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE)
    total_shots = models.PositiveIntegerField()
    total_made = models.PositiveIntegerField()


class WeatherConditions(models.Model):
    temperature = models.IntegerField()
    wind_speed = models.IntegerField()
    conditions = models.CharField(max_length=127)
    humidity = models.IntegerField()
    practice = models.ForeignKey(Practice, on_delete=models.CASCADE, default=1)


class MyUser(User):
    location = models.CharField(max_length=72)


def recalculate_basic_stats(practice_id):
    basic_stats = BasicStats.objects.get(practice_id=practice_id)
    attempts = Attempt.objects.filter(practice_id=practice_id)
    total_made = 0
    total_shots = 0
    for a in attempts:
        total_made += a.attempts_successful
        total_shots += a.attempts

    basic_stats.total_made = total_made
    basic_stats.total_shots = total_shots
    basic_stats.save()
