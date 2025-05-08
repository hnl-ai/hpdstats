# -*- coding: utf-8 -*-
"""The geolocation utility module."""

from decimal import Decimal
import urllib.parse
from dotenv import dotenv_values
import requests
import simplejson as json
from shapely.geometry import Point, box

from .ddb import check_if_item_exists, insert_item

config = dotenv_values('.env')
LOCATIONS_TABLE = 'honolulupd.org-locations'


def geolocate_location(location):
    """Geolocates the given address into lat/lng coordinates."""
    # TODO: Figure out a new way to geolocate the address since MapQuest API's is deprecated
    
    # location = location.strip()

    # if not location:
    #     return {}

    # retrieved_location = check_if_item_exists(
    #     LOCATIONS_TABLE, {'address': location})

    # if retrieved_location:
    #     return retrieved_location

    # oahuBoxPoints = [-158.404958, 21.746884, 21.150598, -157.524172] # Oahu Upper Left, Bottom Right (Lng, Lat)

    # url = 'http://www.mapquestapi.com/geocoding/v1/address?'
    # query_variables = {
    #     'key': config['MAPQUEST_API_KEY'],
    #     'location': location + ', Honolulu, HI', # https://developer.mapquest.com/documentation/common/forming-locations/
    #     'boundingBox': ','.join(map(str, oahuBoxPoints))
    # }

    # url += urllib.parse.urlencode(query_variables)

    # response = requests.get(url)
    # data = response.json()

    obj = {
        'address': location,
        "lat": 0,
        "lng": 0,
    }

    # if not data['info']['statuscode'] == 0:  # Error retrieving location
    #     insert_item(LOCATIONS_TABLE, obj)
    #     return obj
    
    # if not data['results'] or not data['results'][0]['locations']:
    #     insert_item(LOCATIONS_TABLE, obj)
    #     return obj

    # newLat = data['results'][0]['locations'][0]['latLng']['lat']
    # newLng = data['results'][0]['locations'][0]['latLng']['lng']

    # geolocatedPoint = Point(newLat, newLng)
    # oahuBox = box(*oahuBoxPoints)

    # if oahuBox.contains(geolocatedPoint):
    #     obj['lat'] = newLat
    #     obj['lng'] = newLng

    obj = json.loads(json.dumps(obj), parse_float=Decimal)
    # insert_item(LOCATIONS_TABLE, obj)
    return obj
