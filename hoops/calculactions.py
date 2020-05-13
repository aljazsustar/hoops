from scipy.stats import pearsonr
from .models import BasicStats, Practice, User, WeatherConditions
from django.core.exceptions import ObjectDoesNotExist
from sklearn import linear_model
import numpy as np
import math


class Statistics:

    def __init__(self, user_id):
        self.user_id = user_id
        self.shots_made, self.wind_speeds = [], []
        self.practices = Practice.objects.filter(user_id=user_id).order_by('date')
        self.weather = WeatherConditions.objects.all().order_by('wind_speed')
        self.basic_stats = BasicStats.objects.filter(practice__weatherconditions__conditions__isnull=False).order_by('practice__weatherconditions__wind_speed')

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

    def predict(self, w, t, h):
        x = [[we.wind_speed, we.temperature, we.humidity] for we in self.weather]
        y = [s.total_made for s in self.basic_stats]
        regr = linear_model.LinearRegression()
        regr.fit(x, y)
        predicted = regr.predict([[w, t, h]])
        return predicted
