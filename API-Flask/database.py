# database.py
from pymongo import MongoClient
import os


MONGO_URI = os.environ["MONGO_URI"]

client = MongoClient(
    MONGO_URI,
)

db = client.enterprise

db.Articulos.create_index([("NombreArticulo", "text")], default_language="spanish")
db.Clientes.create_index([("NombreCliente", "text")], default_language="spanish")
db.CabeceraAlbaran.create_index([("NombreCliente", "text")], default_language="spanish")
