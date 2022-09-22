import logging
import azure.functions as func
import azure.cosmos.cosmos_client as cosmos_client
import datetime
import json
import os
import uuid

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    # Cria o Client
    client = cosmos_client.CosmosClient(os.environ["HOST"], {'masterKey': os.environ["MASTER_KEY"]})
    db = client.get_database_client(os.environ["DATABASE_ID"])
    
    
    def store_query():
        consult_container = db.get_container_client("consultas")
        payload = {
            'id' : str(uuid.uuid4()),
            'partitionKey' : 'consulta-2',
            'tipoConsulta' : 'Rota',
            'origem': {'type': 'Point', 'coordinates': [req_body["lng"], req_body["lat"]]},
            'destino': req_body["geometry"],
            'localDestino': req_body['local'],
            'tipoDestino': req_body["tipoLocal"],
            'nomeDestino': req_body["nome"],
            'tipoTrajeto': req_body["trajeto"],
            'distancia': req_body["distancia"],
            'dataConsulta': str(datetime.datetime.now())
            }
        consult_container.create_item(body=payload)
        logging.info(f"Registro de Consulta armazenado com id {payload['id']}")
            
    try:
        # Execute Stored Procedure
        # points_container = db.get_container_client("pontos-de-interesse")
        # docs = json.loads(points_container.scripts.execute_stored_procedure(
        #     sproc="uspGetInterests",
        #     params=[req_body],
        #     partition_key="pontos-interesse"
        # ))
        # n = len(docs) if isinstance(docs, list) else 1
        store_query()

        return func.HttpResponse(
            "OK",
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error('\nrun_sample has caught an error. {0}'.format(e))
