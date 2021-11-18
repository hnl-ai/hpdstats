from decimal import Decimal

from ddb_utils import check_if_item_exists, insert_item

from dotenv import dotenv_values
import requests
import simplejson as json

config = dotenv_values('.env')
locations_table_name = 'honolulupd.org-locations'


def geolocate_location(location):
    location = location.strip()
    retrieved_location = check_if_item_exists(
        locations_table_name, {'address': location})

    if not retrieved_location:
        url = 'http://www.mapquestapi.com/geocoding/v1/address?key={}&location={}'.format(
            config['MAPQUEST_API_KEY'], location)
        r = requests.get(url)
        data = r.json()

        if not data['info']['statuscode'] == 0:  # Error retrieving location
            obj = {
                'address': location,
                "lat": 0,
                "lng": 0,
            }
            insert_item(locations_table_name, obj)
            return obj
        obj = {
            'address': location,
            **data['results'][0]['locations'][0]['latLng']
        }
        obj = json.loads(json.dumps(obj), parse_float=Decimal)
        insert_item(locations_table_name, obj)
        return obj
    return retrieved_location
