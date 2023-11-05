from flask import request, jsonify
from extensions import app
from functions.albaranes_f import obtener_por_numero_albaran, obtener_por_nombre_cliente

# http://localhost:5000/api/alb/all?alb=1012
@app.route("/api/alb/all", methods=["GET"])
def get_albaranes_all():
    numero_albaran = request.args.get("alb")
    
    if numero_albaran is None:
        return jsonify({"error": "Parámetro de consulta 'alb' no proporcionado"}), 500
    
    albaran = obtener_por_numero_albaran(numero_albaran)

    if "error" in albaran:
        return jsonify({"error": albaran["error"]}), albaran.get("code", 404)

    return jsonify(albaran)


@app.route(
    "/api/alb/details", methods=["GET"]
)  # http://localhost:5000/api/alb/details?alb=984
def get_albaranes_details():
    numero_albaran = request.args.get("alb")
    albaran = obtener_por_numero_albaran(numero_albaran)

    if not albaran:
        return jsonify({"error": f"Albarán {numero_albaran} no encontrado"}), 404

    cliente = obtener_por_nombre_cliente(albaran["NombreCliente"])
    if not cliente:
        return (
            jsonify({"error": f"Cliente del albarán {numero_albaran} no encontrado"}),
            404,
        )

    detalles = ["NombreCliente", "EMail1", "Telefono"]
    cliente_filtered = {k: cliente[k] for k in detalles if k in cliente}

    return jsonify({"cliente": cliente_filtered})
