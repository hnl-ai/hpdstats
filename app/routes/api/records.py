# -*- coding: utf-8 -*-
"""The api records module."""
import boto3

def create_records_route(app, cache):
    """The api records cache."""
    @cache.cached(timeout=3600, key_prefix='all_records')  # Cache for 1 hour
    def get_all_records():
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('honolulupd.org-records')

        response = table.scan()
        all_records = response['Items']
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            all_records.extend(response['Items'])

        return all_records


    @app.route('/api/records')
    def records_api_route():
        """The api archive route."""
        return {
            "allRecords": get_all_records()
        }
