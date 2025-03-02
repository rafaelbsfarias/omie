from config import Settings
from loguru import logger
from api import Api
from endpoints import Endpoints
from db import Database
from utils.tools import get_total_of_pages, get_body_params_pagination
from utils.constants import HEADERS

settings = Settings()

endpoints = Endpoints()
#endpoints = endpoints.get_all()
endpoints = endpoints.get_endpoint(action="ListarContasCorrentes")
#ListarClientes
#ListarCategorias
#ListarEmpresas
#ListarDepartamentos
#ListarMovimentos
#ListarContasCorrentes

#print("ENDPOINTS", endpoints)

for endpoint in endpoints:
    resource = endpoint.get("resources", None) 
    action = endpoint.get("action", None)
    params = endpoint.get("params", None)
    data_source = endpoint.get("data_source", None)
    page_label = endpoint.get("page_label", None)
    total_of_pages_label = endpoint.get("total_of_pages_label", None)
    records_label = endpoint.get("records_label", None)

    total_of_pages = get_total_of_pages(
        resource,
        action,
        params,
        page_label,
        total_of_pages_label,
        records_label
    )

    records_fetched = 0
    for page in range(1, total_of_pages + 1):
        params[page_label] = page
        
        body = get_body_params_pagination(
            action=action,
            params=params,
            page=page,
            field_pagination=page_label
        )

        api = Api(
            url=f"{settings.BASE_URL}{resource}",
            headers=HEADERS,
            json=body,
            params=params
         )   
        response = api.request(api.post)

        if action == "ListarMovimentos":
            records_fetched += response.get("nRegistros", 0)
            contents = response.get(data_source, [])
        else:
            records_fetched += response.get("registros", 0)
            contents = response.get(data_source, [])

        logger.info(f"Page {page} fetched. Total of records: {records_fetched}")

        db = Database()
        db.save_into_db(page, resource, contents)



