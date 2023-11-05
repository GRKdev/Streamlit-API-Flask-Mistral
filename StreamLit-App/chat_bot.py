import os
import streamlit as st
import requests
import openai
from utils.sidebar_info import display_sidebar_info, display_main_info
from utils.lakera_guard import LakeraGuard

from utils.chatbot_utils import (
    handle_chat_message,
    handle_gpt_ft_message,
    ask_fine_tuned_api,
)

lakera_guard_api_key = st.secrets.get("LAKERA_API", os.getenv("LAKERA_API"))


def chat_bot(username=None):
    DOMINIO = st.secrets.get("DOMINIO", os.getenv("DOMINIO"))
    token = st.session_state["token"]
    headers = {"Authorization": f"Bearer {token}"}
    openai.api_key = st.secrets.get("OPENAI_API_KEY")
    display_main_info()
    display_sidebar_info()

    st.session_state.chat_history = st.session_state.get("chat_history", [])

    if not st.session_state.chat_history:
        st.session_state.chat_history.append(
            {"role": "assistant", "content": "¡Empezemos a chatear!"}
        )

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    lakera_guard = LakeraGuard(lakera_guard_api_key)
    user_input = st.chat_input("Ingresa tu pregunta:")

    if user_input:
        user_input = user_input.strip()

        ## Lakera Guard for prompt injection
        # if lakera_guard.check_prompt_injection(user_input):
        #     st.session_state.chat_history.append(
        #         {"role": "user", "content": user_input}
        #     )
        #     with st.chat_message("user"):
        #         st.markdown(user_input)

        #     error_message = "Mensaje no permitido por motivos de seguridad.🚫"
        #     st.session_state.chat_history.append(
        #         {"role": "assistant", "content": error_message}
        #     )
        #     with st.chat_message("assistant"):
        #         st.error(error_message, icon="⚠️")
        #     return
        # else:
        #     categories, flagged = lakera_guard.check_moderation(user_input)
        #     if flagged:
        #         combined_error_message = lakera_guard.get_error_messages(categories)
        #         st.session_state.chat_history.append(
        #             {"role": "user", "content": user_input}
        #         )
        #         with st.chat_message("user"):
        #             st.markdown(user_input)

        #         error_message = f"Alerta de moderación: {combined_error_message}.🔞"
        #         st.session_state.chat_history.append(
        #             {"role": "assistant", "content": error_message}
        #         )
        #         with st.chat_message("assistant"):
        #             st.error(error_message, icon="⚠️")
        #         return
        ## End of Lakera Guard ##

        # else:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        if (len(user_input) == 12 or len(user_input) == 13) and user_input.isdigit():
            api_response_url = f"/api/art?bar={user_input}"
        else:
            api_response_url = ask_fine_tuned_api(user_input)

        if "api/" in api_response_url:
            full_url = DOMINIO + api_response_url
            try:
                response = requests.get(full_url, headers=headers)
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                response = e.response
                if response.status_code == 403:
                    st.error(
                        "No tienes permisos suficientes para realizar esta acción.",
                        icon="⛔",
                    )
                    return
                elif response.status_code in [
                    400,
                    404,
                    500,
                ]:
                    st.error(
                        f"Error {response.status_code}: {response.reason}",
                        icon="⚠️",
                    )
                    return
            except requests.exceptions.RequestException:
                st.warning("Error de conexión API con endpoint", icon="🔧")
                return
            except Exception as e:
                st.error(f"Ha ocurrido un error inesperado: {e}", icon="🔧")
                return
        else:
            response = None

        with st.chat_message("assistant"):
            message_placeholder = st.empty()

            if response and response.status_code == 200:
                data = response.json()
                handle_chat_message(
                    api_response_url, data, message_placeholder, user_input
                )
            else:
                handle_gpt_ft_message(
                    user_input,
                    message_placeholder,
                    api_response_url,
                    response,
                )