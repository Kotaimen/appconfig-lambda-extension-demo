import json
import urllib.request
import requests
import logging
logging.getLogger().setLevel(logging.DEBUG)

from aws_xray_sdk.core import xray_recorder, patch_all
patch_all()


def lambda_handler(event, context):

    num_exclamations = get_configured_number_of("ExclamationPoints", 1)
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f'Hello world{"!" * num_exclamations}',
        }),
    }


def get_configured_number_of(configuration_type, default):
    try:
        url = f'http://localhost:2772/applications/helloworld/environments/demo/configurations/' + configuration_type
        response = requests.get(url)
        config = response.json()
        logging.debug(config)

        if config.get("enable" + configuration_type, False):
            return config.get("numberOf" + configuration_type, default)
        else:
            return default
    except Exception as e:
        logging.exception(e)
        return default
