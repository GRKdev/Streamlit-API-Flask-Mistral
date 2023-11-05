from database import db
from bson import json_util


def obtener_por_nombre_cliente(
    client_name,
):  # http://localhost:5000/api/cli?info=alvarez,soto
    collection = db["Clientes"]
    search_terms = client_name.split(",")
    search_string = " ".join(['"' + term + '"' for term in search_terms])

    fields = {"NombreCliente": 1, "Telefono": 1, "EMail1": 1, "Comentarios": 1}
    results = collection.find({"$text": {"$search": search_string}}, fields)

    serialized_results = []
    for r in results:
        serialized = json_util.loads(json_util.dumps(r))
        cleaned_serialized = {
            k: v for k, v in serialized.items() if v and str(v).strip() and k != "_id"
        }
        serialized_results.append(cleaned_serialized)

    if not serialized_results:
        return {"error": f"Cliente con nombre: {client_name} no encontrado en DB"}

    return serialized_results


def obtener_telefono_cliente(
    client_name,
):  # http://localhost:5000/api/cli?tlf=alvarez,soto
    collection = db["Clientes"]
    search_terms = client_name.split(",")
    search_string = " ".join(['"' + term + '"' for term in search_terms])
    results = collection.find(
        {"$text": {"$search": search_string}},
        {"NombreCliente": 1, "Telefono": 1, "Telefono2": 1, "EMail1": 1},
    )

    serialized_results = []
    for r in results:
        serialized = json_util.loads(json_util.dumps(r))
        serialized.pop("_id", None)

        cleaned_serialized = {
            k: v
            for k, v in serialized.items()
            if v and (isinstance(v, int) or v.strip())
        }
        serialized_results.append(cleaned_serialized)
    
    return serialized_results


def obtener_email_cliente(
    client_name,
):  # http://localhost:5000/api/cli?mail=alvarez,soto
    collection = db["Clientes"]
    search_terms = client_name.split(",")
    search_string = " ".join(['"' + term + '"' for term in search_terms])
    results = collection.find(
        {"$text": {"$search": search_string}},
        {"NombreCliente": 1, "EMail1": 1, "EMail2": 1, "Telefono": 1},
    )

    serialized_results = []
    for r in results:
        serialized = json_util.loads(json_util.dumps(r))
        serialized.pop("_id", None)

        cleaned_serialized = {
            k: v
            for k, v in serialized.items()
            if v and (isinstance(v, int) or v.strip())
        }
        serialized_results.append(cleaned_serialized)

    if not serialized_results:
        return {"error": f"Cliente con nombre: {client_name} no encontrado en DB"}
    return serialized_results


def obtener_direccion_cliente(
    client_name,
):  # http://localhost:5000/api/cli?dire=alvarez,soto
    collection = db["Clientes"]
    search_terms = client_name.split(",")
    search_string = " ".join(['"' + term + '"' for term in search_terms])
    results = collection.find(
        {"$text": {"$search": search_string}},
        {
            "NombreCliente": 1,
            "Domicilio": 1,
            "Localidad": 1,
            "Municipio": 1,
            "ComunidadAutonoma": 1,
        },
    )

    serialized_results = []
    for r in results:
        serialized = json_util.loads(json_util.dumps(r))
        serialized.pop("_id", None)

        cleaned_serialized = {
            k: v
            for k, v in serialized.items()
            if v and (isinstance(v, int) or v.strip())
        }
        serialized_results.append(cleaned_serialized)

    if not serialized_results:
        return {"error": f"Cliente con nombre: {client_name} no encontrado en DB"}
    
    return serialized_results


def obtener_por_nombre_all(
    client_name,
):  # http://localhost:5000/api/cli?all=alvarez,soto
    collection = db["Clientes"]
    search_terms = client_name.split(",")
    search_string = " ".join(['"' + term + '"' for term in search_terms])
    results = collection.find({"$text": {"$search": search_string}})
    serialized_results = []
    for r in results:
        serialized = json_util.loads(json_util.dumps(r))
        serialized.pop("_id", None)
        cleaned_serialized = {
            k: v
            for k, v in serialized.items()
            if v or (isinstance(v, (str, int, float)) and (v.strip() or k == 'Web'))
        }
        serialized_results.append(cleaned_serialized)
    if not serialized_results:
        return {"error": f"Cliente con nombre: {client_name} no encontrado en DB"}
    return serialized_results


def obtener_por_tlf(phone_number):  # http://localhost:5000/api/cli?clitlf=123456789
    collection = db["Clientes"]
    query = {
        "$or": [
            {"Telefono": {"$regex": f".*{phone_number}$"}},
            {"Telefono2": {"$regex": f".*{phone_number}$"}},
        ]
    }
    projection_fields = {
        "NombreCliente": 1,
        "Telefono": 1,
        "Telefono2": 1,
        "EMail1": 1,
        "_id": 0,
    }
    results = collection.find(query, projection=projection_fields)
    serialized_results = []
    for r in results:
        serialized = json_util.loads(json_util.dumps(r))
        cleaned_serialized = {
            k: v
            for k, v in serialized.items()
            if v and (isinstance(v, int) or v.strip())
        }
        serialized_results.append(cleaned_serialized)
    if not serialized_results:
        return {"error": f"Cliente con telefono: {phone_number} no encontrado en DB"}
    return serialized_results


def obtener_albaranes_por_nombre_cliente(
    nombre_cliente,
):  # http://localhost:5000/api/cli/alb?info=pepito
    collection = db["CabeceraAlbaran"]
    albaranes = (
        collection.find({"NombreCliente": nombre_cliente})
        .sort("FechaAlbaran", -1)
        .limit(10)
    )
    return [json_util.loads(json_util.dumps(albaran)) for albaran in albaranes]
