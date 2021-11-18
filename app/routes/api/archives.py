# -*- coding: utf-8 -*-
"""The api archives module."""
import boto3

def create_archives_route(app, cache):
    """The api archive cache."""
    @cache.cached(timeout=3600, key_prefix='all_archives')
    def get_all_archives():
        bucket = "honolulupd-arrest-logs"
        conn = boto3.client('s3')
        keys = []
        for key in conn.list_objects(Bucket=bucket)['Contents']:
            keys.append(key['Key'])
        return keys


    @app.route('/api/archives')
    def archives_api_route():
        """The api archive route."""
        return {
            "archives": get_all_archives()
        }
