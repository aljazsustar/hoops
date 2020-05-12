from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Practice(models.Model):
    date = models.DateField()
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
    location = models.CharField(max_length=80)


def recalculate_basic_stats(practice_id, attempt_id):
    basic_stats = BasicStats.objects.get(practice_id=practice_id)
    attempt = Attempt.objects.get(id=attempt_id)

    basic_stats.total_made += attempt.attempts_successful
    basic_stats.total_shots += attempt.attempts
    basic_stats.save()
    return BasicStats.objects.get(practice_id=practice_id)


def recalculate_basic_stats_on_delete(practice_id, attempt_id):
    basic_stats = BasicStats.objects.get(practice_id=practice_id)
    attempt = Attempt.objects.get(id=attempt_id)

    basic_stats.total_made -= attempt.attempts_successful
    basic_stats.total_shots -= attempt.attempts
    basic_stats.save()
    return BasicStats.objects.get(practice_id=practice_id)
