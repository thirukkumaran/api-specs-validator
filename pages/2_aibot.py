import streamlit as st
import openai
from streamlit_chat import message as st_message

# Set up OpenAI API key (replace 'YOUR_OPENAI_API_KEY' with your actual key)
openai.api_key = 'test'

# Initialize Streamlit session state for AIbot chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to handle AIbot interactions using ChatCompletion
def interact_with_bot(user_input):
    messages = [
        {"role": "system", "content": "You are a helpful assistant skilled in API validation and documentation."},
        {"role": "user", "content": user_input}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the appropriate model name based on your API subscription
        messages=messages,
        verify=False  # Disable SSL verification
    )
    return response.choices[0].message['content'].strip()

# AIbot Chat Section
st.title("API Guidance Chat")
st.write("Chat with AIbot for help with API validation and documentation!")

# User input text box for AIbot
user_input = st.text_input("You: ", key="user_input")

# Display AIbot messages
if user_input:
    # Get AIbot response
    ai_response = interact_with_bot(user_input)

    # Store the messages
    st.session_state.messages.append({"user": user_input, "bot": ai_response})

    # Clear input box after submission
    st.session_state.user_input = ""

# Show chat history
for msg in st.session_state.messages:
    st_message(msg["user"], is_user=True)
    st_message(msg["bot"], is_user=False)
