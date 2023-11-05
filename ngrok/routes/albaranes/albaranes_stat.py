from flask import request, jsonify
from extensions import app, require_admin_role, require_user_role
from functions.albaranes_f_stat import (
    obtener_fact_por_mes_client_cy,
    obtener_meses_currentyear_fact,
    obtener_meses_selectedyear_fact,
    obtener_anos_meses_fact,
    obtener_anos_meses_ing,
    obtener_ing_por_mes_client_cy,
    obtener_meses_currentyear_ing,
    obtener_meses_selectedyear_ing,
    obtener_fact_por_mes_client_last_3_years,
    obtener_ing_por_mes_client_last_3_years,
)


@app.route("/api/alb_stat", methods=["GET"])
@require_admin_role
def get_albaran_stat():
    params_mapping = {
        "cli_fact_cy": obtener_fact_por_mes_client_cy,
        "cli_fact_3": obtener_fact_por_mes_client_last_3_years,
        "cli_ing_cy": obtener_ing_por_mes_client_cy,
        "cli_ing_3": obtener_ing_por_mes_client_last_3_years,
        "fact_total": obtener_anos_meses_fact,
        "fact_cy": obtener_meses_currentyear_fact,
        "fact_sy": obtener_meses_selectedyear_fact,
        "ing_total": obtener_anos_meses_ing,
        "ing_cy": obtener_meses_currentyear_ing,
        "ing_sy": obtener_meses_selectedyear_ing,
    }

    combined_results = []

    try:
        # Tu lógica de negocio aquí
        for param, function in params_mapping.items():
            value = request.args.get(param)

            if value or (
                param in ["fact_total", "ing_total"] and param in request.args
            ):
                if (
                    param in ["ing_cy", "fact_cy", "fact_total", "ing_total"]
                    and value.lower() != "true"
                ):
                    return jsonify({"error": "Valor no permitido"}), 400

                if param in ["fact_total", "ing_total"]:
                    results = function()
                else:
                    results = function(value)

                if isinstance(results, dict) and "error" in results:
                    return jsonify(results), 404

                if isinstance(results, dict):
                    results = [results]

                combined_results.extend(results)

        return jsonify(combined_results)

    except Exception as e:  # Captura cualquier excepción
        return jsonify({"error": "Error interno del servidor", "details": str(e)}), 500
