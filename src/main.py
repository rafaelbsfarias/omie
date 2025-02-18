from config import Settings
import requests
import json

settings = Settings()

base_url = settings.BASE_URL
app_key = settings.APP_KEY
app_secret = settings.APP_SECRET

resource = "geral/clientes/"
action = 'ListarClientes'
params ={
  "pagina": 1,
  "registros_por_pagina": 50,
  "apenas_importado_api": "N"
}

headers = {
    "Content-Type": "application/json"
}

body = {
    "call":action,
    "app_key":app_key,
    "app_secret":app_secret,
    "param":[params]
    }

response = requests.post(
    url=f"{base_url}{resource}",
    headers=headers,
    json=body
)


if response.status_code == 200:
    content = response.content #json()
    json = response.json()
    total_of_pages = json.get("total_de_paginas", 0)
    records = json.get("total_de_registros", 0)
    print(f"Total of pages: {total_of_pages}")
    print(f"Total of records: {records}")
    with open('output.json', 'wb') as file:
        file.write(content)
else:
    print("Error")


