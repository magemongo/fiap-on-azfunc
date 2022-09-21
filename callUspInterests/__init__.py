from http import client
import logging
import azure.functions as func
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import json
import os


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    location = req_body.get("location")
    lng = req_body.get("lng")
    lat = req_body.get("lat")
    radio = req_body.get("radio")

    # Cria o Client
    client = cosmos_client.CosmosClient(os.environ["HOST"], {'masterKey': os.environ["MASTER_KEY"]})
    db = client.get_database_client(os.environ["DATABASE_ID"])
    container = db.get_container_client(os.environ["CONTAINER_ID"])
            
    try:
        # Execute Stored Procedure
        docs = container.scripts.execute_stored_procedure(
            sproc="uspGetInterests",
            params=[[location, lng, lat, radio]],
            partition_key="pontos-interesse"
        )

        return func.HttpResponse(
            json.dumps(json.loads(docs)),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error('\nrun_sample has caught an error. {0}'.format(e))
