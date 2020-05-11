from scipy.stats import pearsonr
from .models import BasicStats, Practice, User, WeatherConditions
from django.core.exceptions import ObjectDoesNotExist
import math


class Statistics:

    def __init__(self, user_id):
        self.user_id = user_id
        self.shots_made, self.wind_speeds = [], []
        self.practices = Practice.objects.filter(user_id=user_id)

        for p in self.practices:
            try:
                self.wind_speeds.append(WeatherConditions.objects.get(practice_id=p.id).wind_speed)
                self.shots_made.append(BasicStats.objects.get(practice_id=p.id).total_made)
            except ObjectDoesNotExist:
                continue

    def correlation(self):
        if len(self.shots_made) > 1 and len(self.wind_speeds) > 1:
            return pearsonr(self.wind_speeds, self.shots_made) if not math.isnan(
                float(pearsonr(self.wind_speeds, self.shots_made)[0])) else None
