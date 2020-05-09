from requests import get
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
API_KEY = 'dc7f1565a661db4fea351c0858234194'
API_URL = 'http://api.openweathermap.org/data/2.5/weather'


class Weather:

    def __init__(self, location):
        self.location = location
        self.location_key = self.get_location_key()

        if not self.location_key:
            print(f'location {self.location} is not valid!')

    def get_location_key(self):
        with open(os.path.join(BASE_DIR, 'hoops/city.list.json')) as json_file:
            cities = json.load(json_file)

        for city in cities:
            if city['name'].lower() == self.location.lower():
                return city['id']

        return None

    def get_current_conditions(self):
        req = get(API_URL, {'id': self.location_key, 'appid': API_KEY})

        if req.status_code == 200:
            res = req.json()

            return {'temp': res['main']['temp'] - 273.15, 'conditions': res['weather'][0]['main'],
                    'humidity': res['main']['humidity'], 'wind_speed': res['wind']['speed']}

    @staticmethod
    def get_cities():
        with open(os.path.join(BASE_DIR, 'hoops/city.list.json')) as json_file:
            cities = json.load(json_file)

        return [c['name'] for c in cities]