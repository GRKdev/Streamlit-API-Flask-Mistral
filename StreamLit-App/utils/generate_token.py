import jwt
import datetime
import streamlit as st
import os

SECRET_KEY = st.secrets.get("SECRET_KEY", os.getenv("SECRET_KEY"))


class TokenManager:
    def __init__(self):
        # No necesitas mantener el token o expiry_time en el estado si siempre vas a generar uno nuevo.
        pass

    def get_token(self, username):
        # Determinar el rol basado en el nombre de usuario
        role = "user"
        if username in ["admin", "direccio"]:
            role = "admin"
        elif username == "botiga":
            role = "user"
        else:
            st.error("Usuario desconocido, no se puede asignar un token.")

        # Siempre generar un nuevo token
        return self.create_jwt(username, role)

    def create_jwt(self, username, role):
        # El expiry time siempre es 1 día a partir de ahora.
        expiry_time = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        payload = {
            "exp": expiry_time,
            "iat": datetime.datetime.utcnow(),
            "sub": username,
            "role": role,
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
