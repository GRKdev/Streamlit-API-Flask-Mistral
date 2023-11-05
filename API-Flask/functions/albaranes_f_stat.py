from database import db
from datetime import datetime
from constants.constants import MESES


def procesar_resultados(results, output_dict, acumular_total=False):
    total_importe = 0
    for r in results:
        month = r["_id"]["month"]
        importe = round(r["ImporteTotal"], 2)
        output_dict[MESES[month - 1]] = f"{importe} €"
        if acumular_total:
            total_importe += importe
    return total_importe if acumular_total else None


def append_output_if_total_importe_positive(
    output, total_importe, nombre_real_cliente, year, output_dict
):
    if total_importe > 0:
        output.append(
            {
                "NombreCliente": nombre_real_cliente,
                "Año": year,
                "IngresosMensuales": output_dict,
            }
        )


def obtener_fact_por_mes_client_last_3_years(nombre_cliente):
    current_year = datetime.now().year
    collection = db["CabeceraAlbaran"]
    search_terms = nombre_cliente.split(",")
    search_string = " ".join(['"' + term + '"' for term in search_terms])

    nombre_real_cliente = collection.find_one(
        {"$text": {"$search": search_string}}, {"NombreCliente": 1}
    )
    if not nombre_real_cliente:
        return {"error": f"Cliente {nombre_cliente} no encontrado en DB"}

    if nombre_real_cliente:
        nombre_real_cliente = nombre_real_cliente.get("NombreCliente", "")
    else:
        nombre_real_cliente = "Desconocido"

    output = []

    for year in range(current_year - 2, current_year + 1):
        pipeline = [
            {"$match": {"$text": {"$search": search_string}}},
            {
                "$match": {
                    "FechaAlbaran": {
                        "$gte": datetime(year, 1, 1),
                        "$lt": datetime(year + 1, 1, 1),
                    }
                }
            },
            {
                "$group": {
                    "_id": {"month": {"$month": "$FechaAlbaran"}},
                    "ImporteTotal": {"$sum": "$ImporteFactura"},
                }
            },
            {"$sort": {"_id.month": 1}},
        ]

        results = collection.aggregate(pipeline)
        output_dict = {mes: "0 €" for mes in MESES}

        total_importe = procesar_resultados(results, output_dict, acumular_total=True)
        append_output_if_total_importe_positive(
            output, total_importe, nombre_real_cliente, year, output_dict
        )

    return output


def obtener_fact_por_mes_client_cy(
    nombre_cliente,
):  # http://localhost:5000/api/alb_stat?cli_fact_cy=grk
    current_year = datetime.now().year
    collection = db["CabeceraAlbaran"]
    search_terms = nombre_cliente.split(",")
    search_string = " ".join(['"' + term + '"' for term in search_terms])

    nombre_real_cliente = collection.find_one(
        {"$text": {"$search": search_string}}, {"NombreCliente": 1}
    )
    if not nombre_real_cliente:
        return {"error": f"Cliente {nombre_cliente} no encontrado en DB"}
    if nombre_real_cliente:
        nombre_real_cliente = nombre_real_cliente.get("NombreCliente", "")
    else:
        nombre_real_cliente = "Desconocido"

    pipeline = [
        {"$match": {"$text": {"$search": search_string}}},
        {
            "$match": {
                "FechaAlbaran": {
                    "$gte": datetime(current_year, 1, 1),
                    "$lt": datetime(current_year + 1, 1, 1),
                }
            }
        },
        {
            "$group": {
                "_id": {"month": {"$month": "$FechaAlbaran"}},
                "ImporteTotal": {"$sum": "$ImporteFactura"},
            }
        },
        {"$sort": {"_id.month": 1}},
    ]

    results = collection.aggregate(pipeline)
    output_dict = {mes: "0 €" for mes in MESES}
    procesar_resultados(results, output_dict)

    return {
        "NombreCliente": nombre_real_cliente,
        "Año": current_year,
        "IngresosMensuales": output_dict,
    }


def obtener_ing_por_mes_client_cy(
    nombre_cliente,
):  # http://localhost:5000/api/alb_stat?cli_ing_cy=grk
    current_year = datetime.now().year
    collection = db["CabeceraAlbaran"]
    search_terms = nombre_cliente.split(",")
    search_string = " ".join(['"' + term + '"' for term in search_terms])

    nombre_real_cliente = collection.find_one(
        {"$text": {"$search": search_string}}, {"NombreCliente": 1}
    )

    if not nombre_real_cliente:
        return {"error": f"Cliente {nombre_cliente} no encontrado en DB"}
    if nombre_real_cliente:
        nombre_real_cliente = nombre_real_cliente.get("NombreCliente", "")
    else:
        nombre_real_cliente = "Desconocido"

    pipeline = [
        {"$match": {"$text": {"$search": search_string}}},
        {
            "$match": {
                "FechaAlbaran": {
                    "$gte": datetime(current_year, 1, 1),
                    "$lt": datetime(current_year + 1, 1, 1),
                }
            }
        },
        {
            "$group": {
                "_id": {"month": {"$month": "$FechaAlbaran"}},
                "ImporteTotal": {"$sum": "$MargenBeneficio"},
            }
        },
        {"$sort": {"_id.month": 1}},
    ]

    results = collection.aggregate(pipeline)
    output_dict = {mes: "0 €" for mes in MESES}
    procesar_resultados(results, output_dict)

    return {
        "NombreCliente": nombre_real_cliente,
        "Año": current_year,
        "IngresosMensuales": output_dict,
    }


def obtener_ing_por_mes_client_last_3_years(
    nombre_cliente,
):  # http://localhost:5000/api/alb_stat?cli_ing_3=grk
    current_year = datetime.now().year
    collection = db["CabeceraAlbaran"]
    search_terms = nombre_cliente.split(",")
    search_string = " ".join(['"' + term + '"' for term in search_terms])

    nombre_real_cliente = collection.find_one(
        {"$text": {"$search": search_string}}, {"NombreCliente": 1}
    )

    if not nombre_real_cliente:
        return {"error": f"Cliente {nombre_cliente} no encontrado en DB"}
    if nombre_real_cliente:
        nombre_real_cliente = nombre_real_cliente.get("NombreCliente", "")
    else:
        nombre_real_cliente = "Desconocido"

    output = []

    for year in range(current_year - 2, current_year + 1):
        pipeline = [
            {"$match": {"$text": {"$search": search_string}}},
            {
                "$match": {
                    "FechaAlbaran": {
                        "$gte": datetime(year, 1, 1),
                        "$lt": datetime(year + 1, 1, 1),
                    }
                }
            },
            {
                "$group": {
                    "_id": {"month": {"$month": "$FechaAlbaran"}},
                    "ImporteTotal": {"$sum": "$MargenBeneficio"},
                }
            },
            {"$sort": {"_id.month": 1}},
        ]

        results = collection.aggregate(pipeline)
        output_dict = {mes: "0 €" for mes in MESES}

        total_importe = procesar_resultados(results, output_dict, acumular_total=True)
        append_output_if_total_importe_positive(
            output, total_importe, nombre_real_cliente, year, output_dict
        )

    return output


# def obtener_totales_anuales_fact(_=None): #http://localhost:5000/api/alb_stat?fact_total=true
#     collection = db['CabeceraAlbaran']
#     pipeline = [
#         {
#             "$group": {
#                 "_id": {"year": {"$year": "$FechaAlbaran"}},
#                 "ImporteTotal": {"$sum": "$ImporteFactura"}
#             }
#         },
#         {"$sort": {"_id.year": 1}}
#     ]
#     results = collection.aggregate(pipeline)
#     output_list = []

#     for r in results:
#         year = r["_id"]["year"]
#         importe = r["ImporteTotal"]
#         output_list.append({"Año": year, "Cantidad": f"{importe} €"})
#     return {
#         "IngresosAnuales": output_list
# }


def obtener_anos_meses_fact():  # http://localhost:5000/api/alb_stat?fact_total=true
    collection = db["CabeceraAlbaran"]
    pipeline = [
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$FechaAlbaran"},
                    "month": {"$month": "$FechaAlbaran"},
                },
                "ImporteTotal": {"$sum": "$ImporteFactura"},
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}},
    ]
    results = collection.aggregate(pipeline)

    output = []
    current_year = None
    year_data = {}
    total_importe = 0

    for r in results:
        year = r["_id"]["year"]
        month = r["_id"]["month"]
        importe = round(r["ImporteTotal"], 2)

        if current_year != year:
            if year_data and total_importe > 0:
                output.append({"Año": current_year, "IngresosMensuales": year_data})

            year_data = {mes: "0 €" for mes in MESES}
            total_importe = 0
            current_year = year

        year_data[MESES[month - 1]] = f"{importe} €"
        total_importe += importe

    if year_data and total_importe > 0:
        output.append({"Año": current_year, "IngresosMensuales": year_data})

    return output


def obtener_meses_currentyear_fact(
    value=None,
):  # http://localhost:5000/api/alb_stat?fact_cy=true
    current_year = datetime.now().year
    collection = db["CabeceraAlbaran"]
    pipeline = [
        {
            "$match": {
                "FechaAlbaran": {
                    "$gte": datetime(current_year, 1, 1),
                    "$lt": datetime(current_year + 1, 1, 1),
                }
            }
        },
        {
            "$group": {
                "_id": {"month": {"$month": "$FechaAlbaran"}},
                "ImporteTotal": {"$sum": "$ImporteFactura"},
            }
        },
        {"$sort": {"_id.month": 1}},
    ]
    results = collection.aggregate(pipeline)

    output_dict = {mes: "0 €" for mes in MESES}

    for r in results:
        month = r["_id"]["month"]
        importe = round(r["ImporteTotal"], 2)
        output_dict[MESES[month - 1]] = f"{importe} €"

    return {"IngresosMensuales": output_dict, "Año": current_year}


def obtener_meses_selectedyear_fact(
    year,
):  # http://localhost:5000/api/alb_stat?fact_sy=2022
    selected_year = int(year)
    collection = db["CabeceraAlbaran"]
    pipeline = [
        {
            "$match": {
                "FechaAlbaran": {
                    "$gte": datetime(selected_year, 1, 1),
                    "$lt": datetime(selected_year + 1, 1, 1),
                }
            }
        },
        {
            "$group": {
                "_id": {"month": {"$month": "$FechaAlbaran"}},
                "ImporteTotal": {"$sum": "$ImporteFactura"},
            }
        },
        {"$sort": {"_id.month": 1}},
    ]

    results = collection.aggregate(pipeline)
    output_dict = {mes: "0 €" for mes in MESES}

    if not any(results):
        return {"error": f"No se encontraron datos para el año {selected_year}"}

    procesar_resultados(results, output_dict)

    return {"IngresosMensuales": output_dict, "Año": selected_year}


def obtener_anos_meses_ing():  # http://localhost:5000/api/alb_stat?ing_total=true
    collection = db["CabeceraAlbaran"]
    pipeline = [
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$FechaAlbaran"},
                    "month": {"$month": "$FechaAlbaran"},
                },
                "ImporteTotal": {"$sum": "$MargenBeneficio"},
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}},
    ]
    results = collection.aggregate(pipeline)

    output = []
    current_year = None
    year_data = {}
    total_importe = 0

    for r in results:
        year = r["_id"]["year"]
        month = r["_id"]["month"]
        importe = round(r["ImporteTotal"], 2)

        if current_year != year:
            if year_data and total_importe > 0:
                output.append({"Año": current_year, "IngresosMensuales": year_data})

            year_data = {mes: "0 €" for mes in MESES}
            total_importe = 0
            current_year = year

        year_data[MESES[month - 1]] = f"{importe} €"
        total_importe += importe

    if year_data and total_importe > 0:
        output.append({"Año": current_year, "IngresosMensuales": year_data})

    return output


def obtener_meses_currentyear_ing(
    value=None,
):  # http://localhost:5000/api/alb_stat?ing_cy=true
    current_year = datetime.now().year
    collection = db["CabeceraAlbaran"]
    pipeline = [
        {
            "$match": {
                "FechaAlbaran": {
                    "$gte": datetime(current_year, 1, 1),
                    "$lt": datetime(current_year + 1, 1, 1),
                }
            }
        },
        {
            "$group": {
                "_id": {"month": {"$month": "$FechaAlbaran"}},
                "ImporteTotal": {"$sum": "$MargenBeneficio"},
            }
        },
        {"$sort": {"_id.month": 1}},
    ]

    results = collection.aggregate(pipeline)
    output_dict = {mes: "0 €" for mes in MESES}
    procesar_resultados(results, output_dict)

    return {"IngresosMensuales": output_dict, "Año": current_year}


def obtener_meses_selectedyear_ing(
    year,
):  # http://localhost:5000/api/alb_stat?ing_sy=2022
    selected_year = int(year)
    collection = db["CabeceraAlbaran"]
    pipeline = [
        {
            "$match": {
                "FechaAlbaran": {
                    "$gte": datetime(selected_year, 1, 1),
                    "$lt": datetime(selected_year + 1, 1, 1),
                }
            }
        },
        {
            "$group": {
                "_id": {"month": {"$month": "$FechaAlbaran"}},
                "ImporteTotal": {"$sum": "$MargenBeneficio"},
            }
        },
        {"$sort": {"_id.month": 1}},
    ]

    results = collection.aggregate(pipeline)
    output_dict = {mes: "0 €" for mes in MESES}

    if not any(results):
        return {"error": f"No se encontraron datos para el año {selected_year}"}
    
    procesar_resultados(results, output_dict)

    return {"IngresosMensuales": output_dict, "Año": selected_year}
