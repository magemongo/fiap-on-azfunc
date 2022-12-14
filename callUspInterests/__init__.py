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
    
    
    def store_query(n_registros):
        consult_container = db.get_container_client("consultas")
        payload = {
            'id' : str(uuid.uuid4()),
            'partitionKey' : 'consulta-1',
            'tipoConsulta' : 'Explorar',
            'localConsulta': req_body["location"] if "location" in req_body.keys() else None,
            'origem': {'type': 'Point', 'coordinates': [req_body["lng"], req_body["lat"]]},
            'raio': req_body["radio"],
            'qtdDocsRetornados': n_registros,
            'dataConsulta': str(datetime.datetime.now())
            }
        consult_container.create_item(body=payload)
        logging.info(f"Registro de Consulta armazenado com id {payload['id']}")
            
    try:
        # Execute Stored Procedure
        points_container = db.get_container_client("pontos-de-interesse")
        docs = json.loads(points_container.scripts.execute_stored_procedure(
            sproc="uspGetInterests",
            params=[req_body],
            partition_key="pontos-interesse"
        ))
        n = len(docs) if isinstance(docs, list) else 1
        store_query(n)

        return func.HttpResponse(
            json.dumps(docs),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error('\nrun_sample has caught an error. {0}'.format(e))
