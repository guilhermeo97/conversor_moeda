import json

import azure.functions as func
import logging

import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name(name="money_convert")
@app.route(route="money_convert")
def money_convert(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_params = req.params
            pr = req_params.get('pr')
            qtd = req_params.get('qtd')
            response = requests.get(f"https://economia.awesomeapi.com.br/{pr}")
            if response.status_code == 200:
                data = response.json()
                price = data[0]['bid']
                total = float(price) * float(qtd)
                response_body = {
                    "price": price,
                    "quantity": qtd,
                    "total": total
                }
                return func.HttpResponse(body=json.dumps(response_body), status_code=200, mimetype="json")

        except ValueError:
            pass
        else:
            name = req_params.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )