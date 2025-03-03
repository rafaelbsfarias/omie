from pandas import date_range
from src.endpoints import Endpoints
from src.controllers.paginations import PaginationController
from src.db.database import Database

#from db.database import Database
endpoints = Endpoints()
#endpoints = endpoints.get_all()
endpoints = endpoints.get_endpoint(action="ListarExtrato")
#ListarClientes
#ListarCategorias
#ListarEmpresas
#ListarDepartamentos
#ListarMovimentos
#ListarContasCorrentes
#ListarExtrato

#print("ENDPOINTS", endpoints)

for endpoint in endpoints:
    resource = endpoint.get("resources", None) 
    action = endpoint.get("action", None)
    params = endpoint.get("params", None)
    data_source = endpoint.get("data_source", None)
    pagination_type = endpoint.get("pagination_type", "per_page")

    pagination = PaginationController()

    if pagination_type == "date_range":
        depends_on = endpoint.get("depends_on", None)
        
        if depends_on:
            from src.db.database import Database
            db = Database()
            accounts = db.select_from_table(table_name=depends_on, distinct_column="nCodCC")
            print("ACCOUNTS", accounts)
            
            for account in accounts:
                params["nCodCC"] = account
                print("PARAMS", params)
                
                pagination_execute = pagination.pagination(
                    type=pagination_type,
                    resource =resource,
                    action=action,
                    params=params,
                    data_source=data_source
                    )
                

