import streamlit as st
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import logging
import sys
from llama_index.llms.gemini import Gemini
from llama_index.llms.ollama import Ollama

from dotenv import load_dotenv

load_dotenv('..\.env')

Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en-v1.5"
    )
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Settings.llm = Gemini(model="models/gemini-1.5-pro-latest")
Settings.llm = Ollama(model="llama3", request_timeout=60.0)

st.set_page_config(page_title="Chat with the r/indiacoffee, powered by LlamaIndex",
                   page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)

st.title("Chat with the r/indiacoffee, powered by LlamaIndex 💬🦙")
st.info(
    "Check out the subreddit at  [r/indiacoffee](https://www.reddit.com/r/IndiaCoffee/ )", icon="📃")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant",
            "content": "Ask me a question r/indiacoffee subreddit"}
    ]


@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Loading and indexing the  r/indiacoffee subreddit – hang tight! This should take 1-2 minutes."):
        storage_context = StorageContext.from_defaults(persist_dir="embed_dir/")

        index = load_index_from_storage(storage_context)

        return index


index = load_data()

if "chat_engine" not in st.session_state.keys():  # Initialize the chat engine
    st.session_state.chat_engine = index.as_chat_engine(
        chat_mode="condense_question", verbose=True, streaming=True)

# Prompt for user input and save to chat history
if prompt := st.chat_input("Your question"):
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response_stream = st.session_state.chat_engine.chat(prompt)
            st.write(response_stream.response)
            message = {"role": "assistant",
                       "content": response_stream.response}
            # Add response to message history
            st.session_state.messages.append(message)