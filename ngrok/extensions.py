from flask import Flask, request, jsonify
import logging
import jwt
import os
from functools import wraps
from dotenv import load_dotenv

load_dotenv()

SECRET_KEYS = os.environ["SECRET_KEYS"].split(",")

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)


# Decorador para rutas accesibles solo por administradores
def require_admin_role(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]
        for key in SECRET_KEYS:
            try:
                payload = jwt.decode(token, key, algorithms=["HS256"])
                if payload.get("role") == "admin":
                    return f(*args, **kwargs)
                else:
                    logging.error("Acceso denegado. Se requiere rol de administrador.")
                    return jsonify({"message": "Acceso denegado"}), 403
            except jwt.ExpiredSignatureError:
                logging.error("Token expirado.")
                return jsonify({"message": "Token expirado"}), 403
            except jwt.InvalidTokenError:
                continue
        logging.error("Token inválido.")
        return jsonify({"message": "Token inválido"}), 403

    return decorated_function


def is_admin(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return False

    token = auth_header.split(" ")[1]
    for key in SECRET_KEYS:
        try:
            payload = jwt.decode(token, key, algorithms=["HS256"])
            return payload.get("role") == "admin"
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            continue

    return False


def is_user_admin():
    role = request.user_role
    return role == "admin"


# Decorador para rutas accesibles solo por usuarios
def require_user_role(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        token = auth_header.split(" ")[1]
        for key in SECRET_KEYS:
            try:
                payload = jwt.decode(token, key, algorithms=["HS256"])
                if payload.get("role") == "user" or payload.get("role") == "admin":
                    return f(*args, **kwargs)
                else:
                    logging.error("Acceso denegado. Se requiere rol de usuario.")
                    return jsonify({"message": "Acceso denegado"}), 403
            except jwt.ExpiredSignatureError:
                logging.error("Token expirado.")
                return jsonify({"message": "Token expirado"}), 403
            except jwt.InvalidTokenError:
                continue
        logging.error("Token inválido.")
        return jsonify({"message": "Token inválido"}), 403

    return decorated_function


@app.before_request
def before_request_func():
    log_request_info()

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        logging.error(f"Acceso no autorizado: {request.url}")
        return jsonify({"message": "Acceso no autorizado"}), 403

    token = auth_header.split(" ")[1]

    for key in SECRET_KEYS:
        try:
            payload = jwt.decode(token, key, algorithms=["HS256"])
            request.user_role = payload.get(
                "role"
            )  # Asigna el rol del usuario a la solicitud
            return  # Continua con la siguiente operación
        except jwt.ExpiredSignatureError:
            logging.error(f"Token expirado: {token}")
            return jsonify({"message": "Token expirado"}), 403
        except jwt.InvalidTokenError:
            continue  # Prueba con la siguiente clave si la token no es válida

    logging.error(f"Token inválido: {token}")
    return jsonify({"message": "Token inválido"}), 403


@app.errorhandler(404)
def not_found_error(error):
    logging.error(f"Error 404: {error}")
    return jsonify({"error": "Ruta no encontrada"}), 404


@app.errorhandler(500)
def internal_error(error):
    logging.error(f"Error 500: {error}")
    return jsonify({"error": "Error interno del servidor"}), 500


def log_request_info():
    logging.info(f"Petición recibida: {request.method} {request.url}")
    auth_header = request.headers.get("Authorization")
    if auth_header:
        logging.info(f"Cabecera Autorización: {auth_header}")
