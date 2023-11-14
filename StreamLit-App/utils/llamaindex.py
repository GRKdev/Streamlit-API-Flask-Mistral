import pymongo
from llama_index.vector_stores.mongodb import MongoDBAtlasVectorSearch
from llama_index.indices.vector_store.base import VectorStoreIndex
from llama_index.storage.storage_context import StorageContext
from llama_index.readers.file.base import SimpleDirectoryReader
import streamlit as st
import shutil
import os


def save_uploaded_files(uploaded_files):
    temp_folder = "temp_uploaded_files"
    os.makedirs(temp_folder, exist_ok=True)
    saved_paths = []

    for uploaded_file in uploaded_files:
        # Create a file path in the temp folder
        file_path = os.path.join(temp_folder, uploaded_file.name)
        # Write the uploaded file to the new file path
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_paths.append(file_path)

    return saved_paths


def upload_to_vector(files):
    mongo_uri = st.secrets.get("MONGO_URI", os.getenv("MONGO_URI"))
    mongodb_client = pymongo.MongoClient(mongo_uri)
    store = MongoDBAtlasVectorSearch(mongodb_client)
    storage_context = StorageContext.from_defaults(vector_store=store)

    data = SimpleDirectoryReader(input_files=files).load_data()
    index = VectorStoreIndex.from_documents(data, storage_context=storage_context)
