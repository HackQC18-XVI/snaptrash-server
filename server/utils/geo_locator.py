import json
import os
import re
import unicodedata
import math

from geopy.geocoders import Nominatim
from shapely.geometry import Point
from shapely.geometry import shape

from utils.exceptions import HTTPError


SUPPORTED_PICKUP_CITIES = ['montreal']
SUPPORTED_DROPOFF_CITIES = ['quebec', 'sherbrooke']


def norm(word):
    return unicodedata.normalize('NFD', word).encode('ascii', 'ignore').decode('utf-8')


class GeoLocator:

    ROOT_DIR = 'datasets/geojson/'

    def __init__(self, directory=ROOT_DIR):
        self.geojson_files = self.load_files(directory)

    @staticmethod
    def load_files(directory):
        geojson_files = {}
        for city in os.listdir(directory):
            city_dir = os.path.join(directory, city)
            geojson_files[city] = {}
            for method in os.listdir(city_dir):
                geojson_files[city].update({method: {}})
                categories = os.path.join(city_dir, method)
                for filename in os.listdir(categories):
                    if filename.endswith('.json'):
                        with open(os.path.join(categories, filename), 'r') as file:
                            geojson_files[city][method].update({
                                re.sub("\..*$", "", filename): json.load(file)
                            })

        return geojson_files

    def get_pickup_feature(self, type_, latitude, longitude):
        """Get appropriate pickup GeoJSON feature"""
        city = self.get_city_name(latitude, longitude)
        if city not in SUPPORTED_PICKUP_CITIES:
            raise HTTPError(404,
                            f'Requested city: {city} obtained from ({latitude}, {longitude}) not in {SUPPORTED_PICKUP_CITIES}')

        point = Point(longitude, latitude)

        # check each polygon to see if it contains the point
        for feature in self.geojson_files[city]['pickup'][type_]['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                return feature

        return {}

    def get_dropoff_feature(self, type_, latitude, longitude):
        """Get appropriate dropoff GeoJSON feature"""
        city = self.get_city_name(latitude, longitude)
        if city not in SUPPORTED_DROPOFF_CITIES:
            raise HTTPError(404,
                            f'Requested city: {city} obtained from ({latitude}, {longitude}) not found in {SUPPORTED_DROPOFF_CITIES}.')

        features = self.geojson_files[city]['drop'][type_]['features']
        closest_dropoff_feature = min(features,
                                      key=lambda x:self.get_distance(latitude,
                                                                     longitude,
                                                                     x['geometry']['coordinates'][1],
                                                                     x['geometry']['coordinates'][0])
                                    )

        return closest_dropoff_feature

    def get_city_name(self, latitude, longitude):
        """Get the city name corresponding to a given lat and long coord"""
        city_locator = Nominatim()
        city = city_locator.reverse(f'{latitude}, {longitude}')
        return norm(city.raw.get('address').get('city').lower())

    def get_distance(self, lat1, long1, lat2, long2):
        earth_radius_km = 6371;

        deg_lat = math.radians(lat2-lat1)
        deg_long = math.radians(long2-long1)

        lat1 = math.radians(lat1)
        lat2 = math.radians(lat2)

        a = math.sin(deg_lat/2) * math.sin(deg_lat/2) + \
            math.sin(deg_long/2) * math.sin(deg_long/2) * math.cos(lat1) * math.cos(lat2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

        return earth_radius_km * c
