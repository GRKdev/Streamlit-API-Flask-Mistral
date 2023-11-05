from flask import request, jsonify
from extensions import app
from constants.constants import fields_to_sort_clients
from functions.clientes_f import (
    obtener_direccion_cliente,
    obtener_email_cliente,
    obtener_por_nombre_cliente,
    obtener_telefono_cliente,
    obtener_por_nombre_all,
    obtener_por_tlf,
    obtener_albaranes_por_nombre_cliente,
)


@app.route("/api/cli", methods=["GET"])
def get_clientes():
    params_mapping = {
        "info": obtener_por_nombre_cliente,
        "tlf": obtener_telefono_cliente,
        "mail": obtener_email_cliente,
        "dire": obtener_direccion_cliente,
        "all": obtener_por_nombre_all,
        "clitlf": obtener_por_tlf,
    }
    combined_results = []

    for param, function in params_mapping.items():
        for key, value in request.args.items():
            if key.startswith(param):
                results = function(value)

                if "error" in results:
                    return jsonify({"error": results["error"]}), 404

                if isinstance(results, dict):
                    results = [results]
                combined_results.extend(results)

    sorted_combined_results = []
    for cliente in combined_results:
        sorted_cliente = [
            (field, cliente.get(field, None))
            for field in fields_to_sort_clients
            if field in cliente
        ]
        sorted_combined_results.append(sorted_cliente)

    if not sorted_combined_results:
        return (
            jsonify({"error": "Informacion no encontrada en nuestra base de datos"}),
            404,
        )

    return jsonify(sorted_combined_results)


@app.route("/api/cli/alb", methods=["GET"])
def get_info_albaranes():
    nombre_cliente = request.args.get("info")
    cliente = obtener_por_nombre_cliente(nombre_cliente)

    if not cliente:
        return jsonify({"error": f"Cliente {nombre_cliente} no encontrado"}), 404

    primer_cliente = cliente[0] if isinstance(cliente, list) else cliente
    albaranes = obtener_albaranes_por_nombre_cliente(primer_cliente["NombreCliente"])

    if not albaranes:
        return (
            jsonify(
                {"error": f"Albaranes del cliente {nombre_cliente} no encontrados"}
            ),
            404,
        )

    detalles = ["NumeroAlbaran"]
    albaranes_filtered = [
        {k: albaran[k] for k in detalles if k in albaran} for albaran in albaranes
    ]

    return jsonify({"albaranes": albaranes_filtered})
