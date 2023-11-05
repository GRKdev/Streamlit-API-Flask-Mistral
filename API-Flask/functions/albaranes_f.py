from database import db
from utils import mongo_to_json


class AlbaranNotFoundException(Exception):
    pass

def obtener_por_numero_albaran(numero):
    collection = db["CabeceraAlbaran"]

    try:
        num_albaran = int(numero)
    except ValueError:
        return {"error": f"Número de albarán {numero} inválido", "code": 400}

    albaran = collection.find_one({"NumeroAlbaran": num_albaran})
    if albaran:
        return mongo_to_json(albaran)
    else:
        return {"error": f"Albarán {numero} no encontrado en DB", "code": 404}


def obtener_por_nombre_cliente(nombre):
    collection = db["Clientes"]
    cliente = collection.find_one({"NombreCliente": nombre})
    if cliente:
        return mongo_to_json(cliente)
    else:
        return None
