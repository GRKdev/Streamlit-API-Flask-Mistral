import streamlit as st
from openai import OpenAI
import openai
import os
import re
import uuid
import requests
import json
from utils.chart_utils import (
    render_pie_chart_marca,
    render_pie_chart_family,
    render_grouped_bar_chart_fact,
    render_bar_chart_monthly_revenue_monthly_year,
    render_bar_chart_monthly_revenue_client,
    render_bar_chart_monthly_revenue_client_ing,
    render_grouped_bar_chart_ing,
    render_bar_chart_monthly_revenue_monthly_year_ing,
    render_grouped_bar_chart_fact_cli_3_years,
    render_grouped_bar_chart_ing_cli_3_years,
)

from pymongo import MongoClient
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import MongoDBAtlasVectorSearch

# from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI


OPEN_AI_MODEL = st.secrets.get("OPENAI_MODEL", os.getenv("OPENAI_MODEL"))
model_name_ft = st.secrets["OPENAI_MODEL"].split(":")[3].upper()

OPENAI_MODEL_35 = st.secrets.get("OPENAI_MODEL_35", os.getenv("OPENAI_MODEL_35"))
model_name = st.secrets["OPENAI_MODEL_35"].split(":")[3].upper()


HELICONE_AUTH = st.secrets.get("HELICONE_AUTH", os.getenv("HELICONE_AUTH"))

last_assistant_response = None

client = OpenAI()


# def set_api_base(ask_name):
#     if ask_name == "ask_fine_tuned":
#         openai.api_base = "https://oai.hconeai.com/v1"

#     elif ask_name == "ask_gpt":
#         openai.api_base = "https://oai.hconeai.com/v1"
#         # openai.api_base = "http://localhost:1234/v1"

#     elif ask_name == "ask_gpt_ft":
#         openai.api_base = "http://localhost:1234/v1"

#     elif ask_name == "ask_langchain":
#         openai.api_base = "http://localhost:1234/v1"


def ask_fine_tuned_api(prompt):
    # set_api_base("ask_fine_tuned")

    HELICONE_SESSION = (
        st.session_state["user"].title()
        + "-"
        + st.secrets.get("HELICONE_SESSION", os.getenv("HELICONE_SESSION"))
    )

    response = client.completions.create(
        model=OPEN_AI_MODEL,
        prompt=prompt,
        max_tokens=50,
        n=1,
        stop="&&",
        temperature=0,
        # headers={
        #     "Helicone-Auth": HELICONE_AUTH,
        #     "Helicone-Property-Session": HELICONE_SESSION,
        # },
    )
    api_response = response.choices[0].text.strip()

    match = re.search(r"(api/[^ ?]+)(\?.*)?", api_response)

    if match:
        sanitized_response = match.group(0)
    else:
        sanitized_response = api_response
    print(sanitized_response)
    return sanitized_response


def ask_gpt(prompt, placeholder, additional_context=None):
    # set_api_base("ask_gpt")
    user_program = st.session_state["user"].title()
    HELICONE_SESSION = (
        user_program
        + "-"
        + st.secrets.get("HELICONE_SESSION", os.getenv("HELICONE_SESSION"))
    )
    global last_assistant_response

    messages_list = [
        {
            "role": "system",
            "content": "Eres un conector que proporciona información interna de una DB a los usuarios de la empresa. Eres directo y conciso, contestarás en el mismo lenguaje del user. Recibirás una pregunta del User y datos obtenidos de una base de datos. Usarás fuentes para ofrecer una respuesta en formato BULLET POINTS. Proporcionarás una respuesta clara, coherente y útil. Precios en € (ex: 150 €)",
        },
    ]
    if additional_context:
        previous_response = additional_context.get("previous_response")
        if previous_response:
            messages_list.append(
                {"role": "user", "content": f"User: {previous_response}"}
            )
    messages_list.append({"role": "user", "content": f"DataBase Info: {prompt}"})

    full_response = ""

    request_id = str(uuid.uuid4())
    # openai.api_base = ("http://localhost:1234/v1",)
    # openai.base_url = "https://oai.hconeai.com/v1"
    # openai.default_headers = {
    #     "Helicone-Auth": HELICONE_AUTH,
    #     "Helicone-Property-Session": HELICONE_SESSION,
    #     "Helicone-Request-Id": request_id,
    # }
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        # model="local-mode",
        messages=messages_list,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0,
        stream=True,
        user=user_program,
    )
    for part in stream:
        content = part.choices[0].delta.content or ""
        full_response += content
        placeholder.markdown(full_response + "▌")

    placeholder.markdown(full_response)
    last_assistant_response = full_response.strip()

    return last_assistant_response, request_id


def ask_gpt_ft(prompt, placeholder, additional_context=None):
    # set_api_base("ask_gpt_ft")
    HELICONE_SESSION = (
        st.session_state["user"].title()
        + "-"
        + st.secrets.get("HELICONE_SESSION", os.getenv("HELICONE_SESSION"))
    )
    global last_assistant_response
    messages_list = [
        {
            "role": "system",
            "content": "Eres un asistente de la empresa IAND creado por GRKdev. Tienes acceso a datos de clientes y artículos. Recibirás tu respuesta anterior y una pregunta del usuario.",
        },
        {
            "role": "system",
            "content": "Si obtienes 'error' formula una respuesta en base al error y el promp del User. Si te piden más informació aporta lo que tú también sepas en tu conocimiento. el email de soporte es: suport@iand.dev",
        },
    ]
    if last_assistant_response:
        messages_list.append(
            {
                "role": "system",
                "content": f"Assistant last resp: {last_assistant_response}",
            }
        )

    if additional_context:
        api_error = additional_context.get("api_error")
        if api_error is not None:
            messages_list.append({"role": "system", "content": f"Error: {api_error}"})

    messages_list.append({"role": "user", "content": prompt})

    full_response = ""
    request_id = str(uuid.uuid4())

    stream = client.chat.completions.create(
        model=OPENAI_MODEL_35,
        messages=messages_list,
        max_tokens=1000,
        temperature=0,
        stream=True,
    )

    for part in stream:
        content = part.choices[0].delta.content or ""
        full_response += content
        placeholder.markdown(full_response + "▌")

    placeholder.markdown(full_response)
    last_assistant_response = full_response.strip()

    return last_assistant_response


def generate_response_from_mongo_results(data):
    if not data:
        return "No se encontraron resultados."
    else:
        return str(data)


def provide_feedback(heliconeId, rating):
    url = "https://api.hconeai.com/v1/feedback"
    headers = {
        "Helicone-Auth": HELICONE_AUTH,
        "Content-Type": "application/json",
    }
    data = {
        "helicone-id": heliconeId,
        "rating": rating,
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
    except requests.RequestException as e:
        pass


def display_feedback_buttons(request_id):
    def send_thumbs_up_feedback():
        provide_feedback(request_id, True)

    def send_thumbs_down_feedback():
        provide_feedback(request_id, False)

    col_space, thumbs_up, thumbs_down = st.columns([15, 1, 1])
    thumbs_up.button("✔", on_click=send_thumbs_up_feedback)
    thumbs_down.button("✖", on_click=send_thumbs_down_feedback)


def default_handler(data, message_placeholder, user_input):
    json_response = generate_response_from_mongo_results(data)
    additional_context = {
        "previous_response": user_input,
    }
    gpt_response, request_id = ask_gpt(
        json_response, message_placeholder, additional_context=additional_context
    )
    st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
    st.markdown(
        f"<div style='text-align:right; color:green; font-size:small;'>✅ Modelo API: {model_name_ft}. Respuesta elaborada con base de datos y MISTRAL AI en local. Revisa el resultado.</div>",
        unsafe_allow_html=True,
    )

    display_feedback_buttons(request_id)

    return last_assistant_response


def handle_chat_message(api_response_url, data, message_placeholder, user_input):
    api_to_function_map = {
        "api/alb_stat?fact_total=true": render_grouped_bar_chart_fact,
        "api/alb_stat?fact_cy=true": render_bar_chart_monthly_revenue_monthly_year,
        "api/alb_stat?fact_sy=": render_bar_chart_monthly_revenue_monthly_year,
        "api/alb_stat?cli_fact_cy=": render_bar_chart_monthly_revenue_client,
        "api/alb_stat?cli_ing_cy=": render_bar_chart_monthly_revenue_client_ing,
        "api/alb_stat?ing_total=true": render_grouped_bar_chart_ing,
        "api/alb_stat?ing_cy=true": render_bar_chart_monthly_revenue_monthly_year_ing,
        "api/alb_stat?ing_sy=": render_bar_chart_monthly_revenue_monthly_year_ing,
        "api/art_stat?stat=stat_marca": render_pie_chart_marca,
        "api/art_stat?stat=stat_fam": render_pie_chart_family,
        "api/alb_stat?cli_fact_3=": render_grouped_bar_chart_fact_cli_3_years,
        "api/alb_stat?cli_ing_3=": render_grouped_bar_chart_ing_cli_3_years,
    }

    handler = None
    for pattern, func in api_to_function_map.items():
        if api_response_url.startswith(pattern):
            handler = func
            break

    if handler:
        handler(data)
        return None
    else:
        return default_handler(data, message_placeholder, user_input)


def handle_gpt_ft_message(
    user_input, message_placeholder, api_response_url, response=None
):
    # json_api = str(response.json())
    additional_context = {
        "api_error": response.json()["error"] if "api/" in api_response_url else None,
    }
    gpt_response = ask_gpt_ft(
        user_input, message_placeholder, additional_context=additional_context
    )
    st.session_state.chat_history.append({"role": "assistant", "content": gpt_response})
    st.markdown(
        f"<div style='text-align:right; color:red; font-size:small;'>⚠️ Modelo: GPT-3.5-{model_name}. Los datos pueden ser erróneos.</div>",
        unsafe_allow_html=True,
    )
    # display_feedback_buttons(request_id)


class StreamlitCallbackHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs):
        self.text += token
        self.container.markdown(self.text)


def ask_langchain(prompt, placeholder):
    HELICONE_SESSION = (
        st.session_state["user"].title()
        + "-"
        + st.secrets.get("HELICONE_SESSION", os.getenv("HELICONE_SESSION"))
    )
    client = MongoClient(st.secrets.get("MONGO_URI"))
    dbName = "langchain"
    collectionName = "collection_of_text_blobs"
    try:
        # This line checks if you can connect to the MongoDB database
        client.server_info()
    except Exception as e:
        print("There was an error connecting to MongoDB:", e)
        return None  # or handle the error as appropriate for your application

    collection = client[dbName][collectionName]

    openai_api_key = st.secrets.get("OPENAI_API_KEY")

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    vectorstore = MongoDBAtlasVectorSearch(collection, embeddings)

    qa_retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 1},
    )
    request_id = str(uuid.uuid4())

    prompt_template = f"""
    Eres un experto en la documentación de la Empresa IAND. Usa los siguientes datos para responder a la pregunta al final.
    Darás una respuesta clara y concisa con la información del contexto (context) y la pregunta (question) del usuario. No usarás fuentes externas, si no
    sabes la respuesta, contesta "No lo sé" educadamente. Si necesitan más ayuda el email de soporte es: suport@iand.dev.

    Context: {{context}}

    Question: {{question}}

    Answer: 
    """
    PROMPT = PromptTemplate(
        template=prompt_template, input_variables=["context", "question"]
    )
    custom_headers = {
        "Helicone-Auth": HELICONE_AUTH,
        "Helicone-Property-Session": HELICONE_SESSION,
        "Helicone-Request-Id": request_id,
    }
    llm = ChatOpenAI(
        model="gpt-3.5-turbo-1106",
        streaming=True,
        callbacks=[StreamlitCallbackHandler(placeholder)],
        temperature=0,
        openai_api_base="https://oai.hconeai.com/v1",
        # openai_api_base="http://localhost:1234/v1",
        default_headers=custom_headers,
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=qa_retriever,
        chain_type_kwargs={"prompt": PROMPT},
    )

    response = qa(prompt)

    return response, request_id


def handle_langchain_response(user_input, message_placeholder):
    message_placeholder.empty()
    response, request_id = ask_langchain(user_input, message_placeholder)

    response_content = response["result"]

    st.markdown(
        f"<div style='text-align:right; color:yellow; font-size:small;'>📝 Modelo: Documentación LangChain. Los datos pueden ser erróneos.</div>",
        unsafe_allow_html=True,
    )
    st.session_state.chat_history.append(
        {"role": "DOC", "content": response_content, "avatar": "📝"}
    )

    display_feedback_buttons(request_id)
