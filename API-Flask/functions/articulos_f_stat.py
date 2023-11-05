from database import db


def stat_marca():  # http://localhost:5000/api/art_stat?stat=stat_marca
    collection = db["Articulos"]

    pipeline = [{"$group": {"_id": "$Marca", "Cantidad": {"$sum": 1}}}]

    results = collection.aggregate(pipeline)

    serialized_results = []
    for r in results:
        serialized = {"Marca": r["_id"], "Cantidad": r["Cantidad"]}
        serialized_results.append(serialized)

    return serialized_results


def stat_familia():  # http://localhost:5000/api/art_stat?stat=stat_fam
    collection = db["Articulos"]

    pipeline = [{"$group": {"_id": "$Familia", "Cantidad": {"$sum": 1}}}]

    results = collection.aggregate(pipeline)

    serialized_results = []
    for r in results:
        serialized = {"Familia": r["_id"], "Cantidad": r["Cantidad"]}
        serialized_results.append(serialized)

    return serialized_results
