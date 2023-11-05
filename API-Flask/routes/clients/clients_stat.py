from flask import request, jsonify
from extensions import app
from functions.clients_f_stat import stat_cantidad_por_comunidad


@app.route("/api/cli_stat", methods=["GET"])
def get_clients_stats():
    params_mapping = {
        "comu": stat_cantidad_por_comunidad,
    }

    param = request.args.get("stat")
    if param in params_mapping:
        results = params_mapping[param]()
        return jsonify(results)
    else:
        return jsonify({"error": "Parámetro no reconocido o faltante"}), 400
