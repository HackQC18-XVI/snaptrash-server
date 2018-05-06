import json
import os
import re

from shapely.geometry import shape
from shapely.geometry import Point


class GeoLocator:

    ROOT_DIR = 'datasets/geojson/'

    def __init__(self, directory=ROOT_DIR, cities=None):
        cities = cities if cities else []
        self.geojson_files = self.load_files(directory, cities)

    @staticmethod
    def load_files(directory, cities):
        geojson_files = {}
        for city in cities:
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

    def get_feature(self, city, method, type_, latitude, longitude):
        """Get the appropriate feature based on the provided GPS coordinates."""
        point = Point(float(latitude), float(longitude))

        # check each polygon to see if it contains the point
        for feature in self.geojson_files[city][method][type_]['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                return feature

        return {}
