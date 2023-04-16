# -*- coding: utf-8 -*-
"""The api archives module."""
import boto3

def create_archives_route(app, cache):
    """The api archive cache."""
    @cache.cached(timeout=3600, key_prefix='all_archives')
    def get_all_archives():
        bucket = "honolulupd-arrest-logs"
        conn = boto3.client('s3')

        # https://stackoverflow.com/a/59816089/6482196
        paginator = conn.get_paginator('list_objects_v2')
        pages = paginator.paginate(Bucket=bucket)

        keys = []
        for page in pages:
            for obj in page['Contents']:
                keys.append(obj['Key'])
        return keys


    @app.route('/api/archives')
    def archives_api_route():
        """The api archive route."""
        return {
            "archives": get_all_archives()
        }
