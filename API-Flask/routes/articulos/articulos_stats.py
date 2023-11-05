from flask import request, jsonify
from extensions import app
from functions.articulos_f_stat import stat_marca, stat_familia


@app.route("/api/art_stat", methods=["GET"])
def get_articulo_stats():
    params_mapping = {
        "stat_marca": stat_marca,
        "stat_fam": stat_familia,
    }

    param = request.args.get("stat")
    if param in params_mapping:
        results = params_mapping[param]()
        return jsonify(results)
    else:
        return jsonify({"error": "Parámetro no reconocido o faltante"}), 400
