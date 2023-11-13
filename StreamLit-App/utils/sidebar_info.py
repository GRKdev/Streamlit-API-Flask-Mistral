import streamlit as st
import requests
import os
from utils.generate_token import TokenManager
from PIL import Image
import base64
from io import BytesIO

token_manager = TokenManager()


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


def logo():
    logo = Image.open("IMG/logo.png")
    st.sidebar.markdown(
        f'<div style="text-align: center"><img src="data:image/png;base64,{image_to_base64(logo)}" style="width:200px;"></div>',
        unsafe_allow_html=True,
    )


def footer():
    logo_grk = Image.open("IMG/grk_logo.png")
    st.sidebar.divider()
    st.sidebar.markdown(
        f'<h6 style="text-align: center">Made in &nbsp<img src="https://streamlit.io/images/brand/streamlit-mark-color.png" alt="Streamlit logo" height="12">&nbsp by &nbsp<a href="https://github.com/GRKdev"><img src="data:image/png;base64,{image_to_base64(logo_grk)}" alt="GRK" height="16"&nbsp</a></h6>',
        unsafe_allow_html=True,
    )


def clear_chat_history():
    st.session_state.chat_history = []
    st.session_state.last_assistant_response = ""


def display_sidebar_info():
    if "user" in st.session_state:
        user = st.session_state["user"]
        if user == "admin" or user == "direccio":
            st.sidebar.markdown(f"👑 **Administrador**: {user.title()}")
        else:
            st.sidebar.markdown(f"**Usuari:** {user.title()}")

    if st.sidebar.button("Cerrar sesión"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    if user == "admin" or user == "direccio":
        option = st.sidebar.selectbox(
            " ",
            (
                "Ejemplos",
                "Clientes",
                "Artículos",
                "Albaranes",
                "Finanzas",
                "Documentación",
                "Otros",
            ),
        )
    else:
        option = st.sidebar.selectbox(
            " ",
            (
                "Ejemplos",
                "Clientes",
                "Artículos",
                "Albaranes",
                "Documentación",
                "Otros",
            ),
        )

    if option == "Clientes":
        lines = [
            "Dona'm info del client GRK",
            "telefono Maria López",
            "tlf de clientes GRK y Pepito",
            "Toda info cliente John Doe",
            "¿De quién es el tlf 955555555?",
            "Email de Global Data",
            "Quién es el cliente Pedro Muñoz?",
            "Cómo puedo contactar con Gorka Vilar",
            "Adreça de Andorra Telecom",
            "El teléfono 941123456 ¿De quién es?",
            "info de clientes Telecom y Ultra Tech",
        ]

        for line in lines:
            st.sidebar.markdown(f"```markdown\n{line}\n```")

    elif option == "Artículos":
        lineas = [
            "info de articulo Apple",
            "toda info articulo Razer Blackwidow",
            "Precio Venta articulo MacBook Air",
            "Info del artículo 1014",
            "991670248910",
            "art 2021",
            "Dame precio de compra de RTX 3080",
            "quiero toda la info del art 2023",
            "toda la info art 2017, formato lista",
            "Información completa artículo 2024",
            "Stock article Sony WH-1000XM4",
            "Dame la descripcion del articulo airpods",
        ]

        for line in lineas:
            st.sidebar.markdown(f"```markdown\n{line}\n```")

    elif option == "Albaranes":
        lineas = [
            "¿Cuál es el albaran 1012?",
            "Albarán 1014",
            "Albara 1005, quin es el marge",
            "¿Puedo ver el albarán 2023?",
            "ver albaràn 2050",
            "Albaràn 1021, de que cliente es?",
            "Alb 1022 ¿Está facturado?",
            "Albarà 1023, dona'm el nº del pedido",
        ]

        for line in lineas:
            st.sidebar.markdown(f"```markdown\n{line}\n```")

    elif option == "Finanzas":
        lineas = [
            "Facturacion de la empresa",
            "Facturación actual / facturación",
            "Facturacion total / fact total",
            "¿Cuál es la facturación en los últimos años?",
            "Facturacion año 2021",
            "¿Cuánto facturamos en 2022?",
            "Ganancias de la empresa",
            "¿Cuál es nuestra rentabilidad anual hasta la fecha?",
            "Ganancias totales",
            "¿Cuánto hemos ingresado en 2022?",
            "Facturación cliente Pepito grillo",
            "ingresos totales cliente Ultra Tech",
        ]

        for line in lineas:
            st.sidebar.markdown(f"```markdown\n{line}\n```")

    elif option == "Documentación":
        lineas = [
            "DOC Dame la operativa de llamadas enumerando puntos",
            "!Hazme resumen del chatbot",
            "Doc hazme una plantilla de email de problema de conexión",
            "doc ¿Cuál es la operativa para responder un email?",
            "!cómo se llama el programa de ticketing? enumera los puntos de como utilizarlo",
            "!Tecnologías y Roadmap del proyecto, que se ha cumplido y que no? marca con un check y dame links",
            "!¿Qué podemos hacer con el chatbot?",
            "!Operativa flujo de trabajo con emails porfavor",
        ]

        for line in lineas:
            st.sidebar.markdown(f"```markdown\n{line}\n```")
    elif option == "Otros":
        lineas = [
            "¿Qué es iand.dev?",
            "Quien ha creado el chatbot?",
            "¿Cómo funciona este chat?",
            "Los datos son inventados?",
            "¿Cómo te conectas a la DB?",
            "Hi ha algun tipus de revisió humana?",
            "Sobre qué puedo preguntarte?",
            "Quién está detrás de tu desarrollo?",
            "¿Cómo puedo reportar un error?",
            "¡Eres terrible!",
        ]

        for line in lineas:
            st.sidebar.markdown(f"```markdown\n{line}\n```")

    st.sidebar.button("Borrar Historial", on_click=clear_chat_history)

    footer()


def display_main_info():
    st.info(
        """
        #### **Bienvenido al chatbot de IAND**

        Este chatbot inteligente te permite hacer consultas directas con lenguaje natural a nuestra base de datos de MongoDB y en la documentación de la empresa.

        ##### ¿Qué puedes hacer?
        - 👤 **Clientes**: Buscar información detallada de clientes.
        - 🛒 **Artículos**: Consultar detalles de artículos, incluyendo precios y stock.
        - 🧾 **Albaranes**: Obtener información sobre albaranes específicos.
        - 📊 **Finanzas**: Consultas de facturación e ingresos de la empresa y cliente, este resultado se realiza sin pasar por GPT-3.5, directo de la API.
        - 📝 **Documentación**: Buscar en la documentación de la empresa. Para activar empezar la conversación con **DOC**, **doc** o **!**.

        ⬅️ **Ejemplos de preguntas** que puedes hacer se encuentran en el menú de la izquierda.
        """
    )
