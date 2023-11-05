from database import db


def stat_cantidad_por_comunidad():  # http://localhost:5000/api/cli_stat?stat=comu
    collection = db["Clientes"]

    pipeline = [{"$group": {"_id": "$ComunidadAutonoma", "Cantidad": {"$sum": 1}}}]

    results = collection.aggregate(pipeline)

    serialized_results = []
    sin_data_count = 0

    for r in results:
        if r["_id"] is None:
            sin_data_count += r["Cantidad"]
        else:
            serialized = {"ComunidadAutonoma": r["_id"], "Cantidad": r["Cantidad"]}
            serialized_results.append(serialized)

    if sin_data_count > 0:
        serialized_results.append(
            {"ComunidadAutonoma": "Sin DATA", "Cantidad": sin_data_count}
        )

    return serialized_results
