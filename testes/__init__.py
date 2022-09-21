import azure.functions as func

def main(req: func.HttpRequest, doc: func.Out[func.Document]) -> func.HttpResponse:
    request_body = req.get_body()

    doc.set(func.Document.from_json(request_body))

    return 'OK'