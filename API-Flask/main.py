from extensions import app
from routes.albaranes import albaranes_stat, albaranes
from routes.articulos import articulos_stats, articulos
from routes.clients import clients, clients_stat

if __name__ == "__main__":
    for rule in app.url_map.iter_rules():
        print(f"{rule} -> {rule.endpoint}")
    app.run(debug=True)
