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

# Configuration: API Key and Base URL
API_KEY = os.getenv("API_KEY")
BASE_URL = "https://litellm.govtext.gov.sg"

# Ensure Python uses certifi's CA bundle for SSL handling
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

# Verify API key exists
if not API_KEY:
    st.error("API Key not found. Please add it to the .env file.")
    st.stop()

def check_password():
    """Returns `True` if the user had the correct password."""
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    return False

# Ensure password protection is active
if not check_password():
    st.stop()  # Do not continue if check_password is not True.
    
class CustomEmbeddings(Embeddings):
    """Custom embedding class to fetch embeddings from your model."""
    
    def embed_documents(self, texts):
        """Embed multiple documents."""
        input_json = {
            "model": "text-embedding-3-small-prd-gcc2-lb",
            "input": texts  # Verify that this format is correct according to API documentation
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
            "User-Agent": "Mozilla/5.0"
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/embeddings",
                json=input_json,
                headers=headers,
                verify=False  # Adjust SSL handling as needed
            )
            response.raise_for_status()  # Raises an error for HTTP status codes 400 or above

            # Process and validate response data
            embedding_data = response.json().get("data", [])
            if not embedding_data:
                st.error("No embedding data returned from the server.")
                return []  # Return an empty list to handle gracefully
            
            # Return the embeddings list
            return [item["embedding"] for item in embedding_data]
        
        except requests.RequestException as e:
            st.error(f"Embedding error: {e}")
            # Log response text for debugging if available
            st.write("Response content:", getattr(e.response, "text", "No response content"))
            return []

    def embed_query(self, text):
        """Embed a single query."""
        embeddings = self.embed_documents([text])
        if embeddings:
            return embeddings[0]  # Safely access the first embedding if available
        else:
            st.error("Failed to retrieve embeddings for query.")
            return None  # Return None if no embeddings are available


def init_faiss():
    """Initialize FAISS index and load from file cache if available."""
    index_path = "faiss_index.pkl"
    content_folder = "content"

    # Check if content exists
    if not os.listdir(content_folder):
        st.error("Content folder is empty. Please add documents to 'content/' directory.")
        st.stop()

    # Load from cache if index file exists and content is not modified
    files_modified = max(
        os.path.getmtime(os.path.join(content_folder, f))
        for f in os.listdir(content_folder)
    )
    if os.path.exists(index_path) and os.path.getmtime(index_path) >= files_modified:
        with open(index_path, "rb") as f:
            return pickle.load(f)

    # Load and process documents if cache is not available
    loaders = [TextLoader(os.path.join(content_folder, f)) for f in os.listdir(content_folder)]
    splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=30)
    docs = [Document(page_content=doc.page_content) for loader in loaders for doc in loader.load_and_split(splitter)]

    # Create FAISS index
    embeddings_model = CustomEmbeddings()
    faiss_index = FAISS.from_documents(docs, embeddings_model)

    # Save FAISS index to file
    with open(index_path, "wb") as f:
        pickle.dump(faiss_index, f)

    return faiss_index

def query_custom_model(prompt, context):
    """Query the custom model with user input and context."""
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
        "Authorization": f"Bearer {API_KEY}",
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            json={"model": "gpt-4o-prd-gcc2-lb", "messages": messages},
            headers=headers,
            verify=False  # Disable SSL verification for testing
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
