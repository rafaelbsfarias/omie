from config import Settings
import requests
import json

settings = Settings()
base_url = settings.BASE_URL
app_key = settings.APP_KEY
app_secret = settings.APP_SECRET

endpoints = [
    {
        "resources":"geral/clientes/",
        "action":'ListarClientes',
        "params":{
            "pagina": 1,
            "registros_por_pagina": 50,
            "apenas_importado_api": "N"
        } 
    }
]


HEADERS = {
    "Content-Type": "application/json"
}

def request(resource: str, body: dict, params: dict) -> dict:
    response = requests.post(
        url=f"{base_url}{resource}",
        headers=HEADERS,
        json=body,
        params=params
    )
    if response.status_code == 200:
        json = response.json()
        return json
    else:
        raise Exception (f"Error: {response.status_code}")


def get_total_of_pages(resource: str, action: str, params: dict) -> int:
    payload = {
        "call": action,
        "app_key": app_key,
        "app_secret": app_secret,
        "param": [params]
    }
    response = request(resource, payload, params)
    total_of_pages = response.get("total_de_paginas", 0)
    records = response.get("total_de_registros", 0)
    print(f"Total of records: {records}")

    return total_of_pages

for endpoint in endpoints:
    resource = endpoint.get("resources", None) 
    action = endpoint.get("action", None)
    params = endpoint.get("params", None)

    total_of_pages = get_total_of_pages(resource, action, params)
    print(f"Total of pages: {total_of_pages}")

    records_fetched = 0
    for page in range(1, total_of_pages + 1):
        params["pagina"] = page
        
        body = {
            "call": action,
            "app_key": app_key,
            "app_secret": app_secret,
            "param": [params]
        }

        response = request(resource, body, params)
        records_fetched += response.get("registros", 0)

        print(f"Page: {page}", f"Records: {records_fetched}")


#if response.status_code == 200:
#
#    with open('output.json', 'wb') as file:
#        file.write(content)
#else:
#    print("Error")
#

