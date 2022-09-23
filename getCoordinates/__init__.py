import logging
from urllib import response
import requests
import azure.functions as func
import os
import json


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    address = req.params.get("address")
    bing_key = os.environ["BINGMAPS_KEY"]
    url = f"http://dev.virtualearth.net/REST/v1/Locations/BR/SP/{address}?maxResults=1&key={bing_key}"

    response_body = requests.request("GET", url).json()
    coordinates = response_body["resourceSets"][0]["resources"][0]["point"]["coordinates"]
    response = {
        "lat": coordinates[0],
        "lng": coordinates[1]
    }

    return func.HttpResponse(
            json.dumps(response),
            status_code=200
    )
    
