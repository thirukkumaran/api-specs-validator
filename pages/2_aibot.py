import streamlit as st
from streamlit_chat import message as st_message  # Correct import for st_message
from langchain.vectorstores import FAISS
from langchain.embeddings.base import Embeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.schema import Document
from dotenv import load_dotenv
import hmac
import requests
import pickle
import os
import certifi  # Proper SSL handling with certifi

# Load environment variables from .env file
load_dotenv()

# Configuration: API Key and OpenAI API endpoint
API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_EMBEDDINGS_URL = "https://api.openai.com/v1/embeddings"
OPENAI_CHAT_URL = "https://api.openai.com/v1/chat/completions"

# Ensure Python uses certifi's CA bundle for SSL handling
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# Verify API key exists
if not API_KEY:
    st.error("API Key not found. Please add it to the .env file.")
    st.stop()

def check_password():
    """Returns True if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if st.session_state.get("password_correct", False):
        return True

    st.text_input("Password", type="password", on_change=password_entered, key="password")
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

if not check_password():
    st.stop()

class CustomOpenAIEmbeddings(Embeddings):
    """Embedding class to fetch embeddings using direct OpenAI API call with verify=False."""
    def embed_documents(self, texts):
        """Embed multiple documents."""
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        try:
            response = requests.post(
                OPENAI_EMBEDDINGS_URL,
                json={"input": texts, "model": "text-embedding-ada-002"},
                headers=headers,
                verify=False  # Disable SSL verification
            )
            response.raise_for_status()
            return [item["embedding"] for item in response.json().get("data", [])]
        except requests.RequestException as e:
            st.error(f"Embedding error: {e}")
            return []

    def embed_query(self, text):
        """Embed a single query."""
        embeddings = self.embed_documents([text])
        return embeddings[0] if embeddings else None

@st.cache_resource(show_spinner=True)
def init_faiss():
    """Initialize FAISS index and load from cache if available."""
    index_path = "faiss_index.pkl"
    content_folder = "content"

    if not os.listdir(content_folder):
        st.error("Content folder is empty. Please add documents to 'content/' directory.")
        st.stop()

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

    embeddings_model = CustomOpenAIEmbeddings()
    faiss_index = FAISS.from_documents(docs, embeddings_model)

    with open(index_path, "wb") as f:
        pickle.dump(faiss_index, f)

    return faiss_index

def query_custom_model(prompt, context):
    """Query the OpenAI chat model with user input and context."""
    messages = [
        {"role": "system", "content": (
            "You are an expert assistant that answers questions strictly using the provided context. "
            "Extract relevant information and provide the best answer. Make educated guesses if needed."
        )},
        {"role": "system", "content": f"Context:\n{context}"},
        {"role": "user", "content": prompt},
    ]
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    try:
        response = requests.post(
            OPENAI_CHAT_URL,
            json={"model": "gpt-4-turbo", "messages": messages},
            headers=headers,
            verify=False  # Disable SSL verification
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except requests.RequestException as e:
        st.error(f"Chat request failed: {e}")
        return "I'm sorry, I couldn't process your request."

def interact_with_bot(user_input):
    """Handle chat interaction using FAISS and custom model."""
    if "faiss_index" not in st.session_state:
        st.session_state.faiss_index = init_faiss()

    docs = st.session_state.faiss_index.similarity_search(user_input, k=5)
    context = "\n".join([doc.page_content for doc in docs])
    if not context:
        return "No relevant context found."
    return query_custom_model(user_input, context)

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("API Guidance Chat")
st.write("Chat for guidance on API strategy, design, security, and more!")

def get_user_input():
    """Capture user input via Streamlit form."""
    with st.form(key="user_input_form"):
        user_input = st.text_input("You:")
        submit_button = st.form_submit_button(label="Send")
    return user_input if submit_button else None

user_input = get_user_input()

if user_input:
    ai_response = interact_with_bot(user_input)
    st.session_state.messages.insert(0, {"user": user_input, "bot": ai_response})

# Display chat history
for index, msg in enumerate(st.session_state.messages):
    st_message(msg["user"], is_user=True, key=f"user_{index}")
    st_message(msg["bot"], is_user=False, key=f"bot_{index}")
