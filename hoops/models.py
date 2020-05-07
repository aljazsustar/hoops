from django.db import models
from django.utils import timezone


class Practice(models.Model):
    date = models.DateField(default=timezone.now().date())


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
