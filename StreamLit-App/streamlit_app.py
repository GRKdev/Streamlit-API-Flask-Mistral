import streamlit as st
from utils.auth import check_password
from utils.sidebar_info import logo

st.set_page_config(
    page_title="Chatbot - GRK",
    page_icon="IMG/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"About": "# **GRKdev** v1.2.0"},
)

if not check_password():
    st.stop()

from chat_bot import chat_bot  # noqa: E402

if "user" in st.session_state and st.session_state["user"]:
    logo()
    chat_bot(st.session_state["user"])
else:
    st.write("Usuario no autenticado o estado de sesión 'user' no establecido.")
