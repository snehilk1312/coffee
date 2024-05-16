from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.gemini import Gemini
from llama_index.core import StorageContext, load_index_from_storage
import streamlit as st
from dotenv import load_dotenv


Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )

load_dotenv('..\.env')
Settings.llm = Gemini(model="models/gemini-1.5-pro-latest")

@st.cache_resource
def load_model():

    storage_context = StorageContext.from_defaults(persist_dir="embed_dir/")

    index = load_index_from_storage(storage_context)

    return index.as_query_engine()


query_engine = load_model()


question = st.text_input('Enter your question here')

if question:
    
    response = query_engine.query(question)
    
    st.write(response.response)