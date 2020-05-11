from scipy.stats import pearsonr
from .models import BasicStats, Practice, User, WeatherConditions
from django.core.exceptions import ObjectDoesNotExist
import math


class Statistics:

    def __init__(self, user_id):
        self.user_id = user_id
        self.shots_made, self.wind_speeds = [], []
        self.practices = Practice.objects.filter(user_id=user_id).order_by('date')
        self.weather = WeatherConditions.objects.all().order_by('wind_speed')
        self.basic_stats = BasicStats.objects.all().order_by('practice__weatherconditions__wind_speed')

        for w in self.weather:
            try:
                self.wind_speeds.append(w.wind_speed)
                self.shots_made.append(self.basic_stats.get(practice_id=w.practice.id).total_made)
            except ObjectDoesNotExist:
                continue

    def correlation(self):
        if len(self.shots_made) > 1 and len(self.wind_speeds) > 1:
            return pearsonr(self.wind_speeds, self.shots_made) if not math.isnan(
                float(pearsonr(self.wind_speeds, self.shots_made)[0])) else None
