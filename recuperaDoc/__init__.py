import logging
import azure.functions as func
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.partition_key import PartitionKey
import json

HOST = 'https://fiap-on-challange.documents.azure.com:443/'
MASTER_KEY = '4uB0eu5ynq8poRAOCHwO4V2eiA1PYmETpnwXd2aqwI93tHH1JvgFRqexhnoIwuloZYZUjT3JEekrE9KK3U16jQ=='
DATABASE_ID = 'Challenge'
CONTAINER_ID = 'pontos-de-interesse'


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()
    location = req_body.get("location")
    lng = req_body.get("lng")
    lat = req_body.get("lat")
    radio = req_body.get("radio")

    # Cria o Client
    client = cosmos_client.CosmosClient(HOST, {'masterKey': MASTER_KEY})

    # Encontra o Database e Collection
    try:
        # setup database for this sample
        try:
            db = client.create_database(id=DATABASE_ID)
            print('Database with id \'{0}\' created'.format(DATABASE_ID))

        except exceptions.CosmosResourceExistsError:
            db = client.get_database_client(DATABASE_ID)
            print('Database with id \'{0}\' was found'.format(DATABASE_ID))

        # setup container for this sample
        try:
            container = db.create_container(id=CONTAINER_ID, partition_key=PartitionKey(path='/partitionKey'))
            print('Container with id \'{0}\' created'.format(CONTAINER_ID))

        except exceptions.CosmosResourceExistsError:
            container = db.get_container_client(CONTAINER_ID)
            print('Container with id \'{0}\' was found'.format(CONTAINER_ID))

    except exceptions.CosmosHttpResponseError as e:
        print('\nrun_sample has caught an error. {0}'.format(e.message))

    # Execute Stored Procedure
    docs = container.scripts.execute_stored_procedure(
        sproc="testeProc",
        params=[[location, lng, lat, radio]],
        partition_key="pontos-interesse"
    )

    return func.HttpResponse(
        json.dumps(docs),
        status_code=200,
        mimetype="application/json"
    )
