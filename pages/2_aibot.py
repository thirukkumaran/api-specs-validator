import streamlit as st
from streamlit_chat import message as st_message
import openai
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
from dotenv import load_dotenv
import pickle
import os
import certifi

# Ensure proper certificate handling
os.environ['CURL_CA_BUNDLE'] = ''

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    st.error("OpenAI API key is not set. Please add it to the .env file.")
    st.stop()

# Initialize FAISS with caching and auto-refresh if files are updated
@st.cache_resource
def init_faiss():
    index_path = "faiss_index.pkl"
    content_folder = "content"

    # Check if FAISS index needs to be rebuilt
    files_modified = max(
        os.path.getmtime(os.path.join(content_folder, f))
        for f in os.listdir(content_folder)
    )

    if os.path.exists(index_path) and os.path.getmtime(index_path) >= files_modified:
        with open(index_path, "rb") as f:
            return pickle.load(f)

    # Load and split markdown files into smaller chunks
    loaders = [TextLoader(os.path.join(content_folder, f)) for f in os.listdir(content_folder)]
    splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=30)
    docs = [doc for loader in loaders for doc in loader.load_and_split(splitter)]

    # Use the latest OpenAI embedding model for FAISS
    embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
    faiss_index = FAISS.from_documents(docs, embeddings)

    # Save the FAISS index for future use
    with open(index_path, "wb") as f:
        pickle.dump(faiss_index, f)

    return faiss_index

# Query OpenAI with the user input and context
def query_openai(prompt, context):
    messages = [
        {"role": "system", "content": (
            "You are an expert assistant that answers questions strictly using the provided context. "
            "Try to extract relevant information from the context to provide the best possible answer. "
            "If the answer is not directly in the context, make an educated guess based on it."
        )},
        {"role": "system", "content": f"Context:\n{context}"},
        {"role": "user", "content": prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=messages,
        temperature=0.3
    )
    return response.choices[0].message['content'].strip()

# Interact with the bot using FAISS and OpenAI
def interact_with_bot(user_input):
    if "faiss_index" not in st.session_state:
        st.session_state.faiss_index = init_faiss()

    # Retrieve relevant documents (increased k for broader context)
    docs = st.session_state.faiss_index.similarity_search(user_input, k=10)
    context = "\n".join([doc.page_content for doc in docs])

    # Debug: Print the retrieved context
    if not context.strip():
        print("No relevant context found.")
        return "I'm sorry, I couldn't find relevant information in the provided content."

    print(f"Retrieved Context:\n{context}")

    # Generate response with OpenAI using the retrieved context
    return query_openai(user_input, context)

# Initialize session state for messages if not set
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit UI
st.title("API Guidance Chat")
st.write("Chat with AIbot for guidance on API strategy, design, security, and more!")

# Input form to capture user input
def get_user_input():
    with st.form(key="user_input_form"):
        user_input = st.text_input("You:")
        submit_button = st.form_submit_button(label="Send")
    return user_input if submit_button else None

# Get user input
user_input = get_user_input()

if user_input:
    # Get AIbot's response
    ai_response = interact_with_bot(user_input)

    # Store the conversation in session state (new messages at the start)
    st.session_state.messages.insert(0, {"user": user_input, "bot": ai_response})

# Display chat history with unique keys for each message
for index, msg in enumerate(st.session_state.messages):
    st_message(msg["user"], is_user=True, key=f"user_{index}")
    st_message(msg["bot"], is_user=False, key=f"bot_{index}")
