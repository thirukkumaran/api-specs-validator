import streamlit as st
from streamlit_chat import message as st_message  # Correct import for st_message
from langchain.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.schema import Document
from dotenv import load_dotenv
import requests
import pickle
import os

# Load environment variables from .env file
load_dotenv()

# Configuration: API Key and Base URL
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://litellm.govtext.gov.sg"

os.environ['CURL_CA_BUNDLE'] = ''  # Ensure SSL handling if needed

class CustomEmbeddings(Embeddings):
    """Custom embedding class to fetch embeddings from your model."""
    def embed_documents(self, texts):
        input_json = {"model": "text-embedding-3-small-prd-gcc2-lb", "input": texts}
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.post(f"{BASE_URL}/embeddings", json=input_json, headers=headers)
        if response.status_code == 200:
            return [item["embedding"] for item in response.json()["data"]]
        else:
            st.error(f"Embedding error: {response.text}")
            return []

    def embed_query(self, text):
        """Embed a single query."""
        return self.embed_documents([text])[0]

@st.cache_resource(show_spinner=True)
def init_faiss():
    index_path = "faiss_index.pkl"
    content_folder = "content"
    files_modified = max(
        os.path.getmtime(os.path.join(content_folder, f))
        for f in os.listdir(content_folder)
    )
    if os.path.exists(index_path) and os.path.getmtime(index_path) >= files_modified:
        with open(index_path, "rb") as f:
            return pickle.load(f)

    loaders = [TextLoader(os.path.join(content_folder, f)) for f in os.listdir(content_folder)]
    splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=30)
    docs = [Document(page_content=doc.page_content) for loader in loaders for doc in loader.load_and_split(splitter)]

    embeddings_model = CustomEmbeddings()
    faiss_index = FAISS.from_documents(docs, embeddings_model)

    with open(index_path, "wb") as f:
        pickle.dump(faiss_index, f)

    return faiss_index

def query_custom_model(prompt, context):
    messages = [
        {"role": "system", "content": (
            "You are an expert assistant that answers questions strictly using the provided context. "
            "Try to extract relevant information from the context to provide the best possible answer. "
            "If the answer is not directly in the context, make an educated guess based on it."
        )},
        {"role": "system", "content": f"Context:\n{context}"},
        {"role": "user", "content": prompt},
    ]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.post(
        f"{BASE_URL}/chat/completions", json={"model": "gpt-4o-prd-gcc2-lb", "messages": messages}, headers=headers
    )
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"].strip()
    else:
        st.error(f"Chat error: {response.text}")
        return "I'm sorry, I couldn't process your request."

def interact_with_bot(user_input):
    if "faiss_index" not in st.session_state:
        st.session_state.faiss_index = init_faiss()

    docs = st.session_state.faiss_index.similarity_search(user_input, k=5)
    context = "\n".join([doc.page_content for doc in docs])
    if not context:
        return "No relevant context found."
    return query_custom_model(user_input, context)

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("API Guidance Chat")
st.write("Chat with AIbot for guidance on API strategy, design, security, and more!")

def get_user_input():
    with st.form(key="user_input_form"):
        user_input = st.text_input("You:")
        submit_button = st.form_submit_button(label="Send")
    return user_input if submit_button else None

user_input = get_user_input()

if user_input:
    ai_response = interact_with_bot(user_input)
    st.session_state.messages.insert(0, {"user": user_input, "bot": ai_response})

for index, msg in enumerate(st.session_state.messages):
    st_message(msg["user"], is_user=True, key=f"user_{index}")
    st_message(msg["bot"], is_user=False, key=f"bot_{index}")
