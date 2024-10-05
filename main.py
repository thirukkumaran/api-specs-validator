import streamlit as st
import json
import yaml
from jsonschema import validate, ValidationError
import openai
from dotenv import load_dotenv
import os

# Load environment variables and set up OpenAI API key
load_dotenv('.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

# Load OpenAPI standard schema from external JSON file
with open("openapi_standard.json", "r") as f:
    openapi_standard = json.load(f)

# Function to validate API specs and return simplified error messages
def validate_api_spec(api_spec):
    try:
        validate(instance=api_spec, schema=openapi_standard)
        return "API Spec is valid!", True, []
    except ValidationError as e:
        # Extract relevant error information
        error_path = " -> ".join([str(x) for x in list(e.path)]) if e.path else "Unknown path"
        error_message = f"Error at {error_path}: {e.message}"
        return "API Spec is invalid.", False, [error_message]

# Function to generate documentation using ChatCompletion
def generate_documentation(api_spec):
    # Using a conversation-based prompt for ChatCompletion
    messages = [
        {"role": "system", "content": "You are a helpful assistant skilled in creating API documentation."},
        {"role": "user", "content": f"Generate a standardized API documentation for the following spec:\n{json.dumps(api_spec, indent=2)}"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use the appropriate model name based on your API subscription
        messages=messages,
        verify=False  # Disable SSL verification
    )
    return response.choices[0].message['content'].strip()

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

# Sidebar menu for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["API Spec Validator", "API Guidance Chat"])

# Display the selected page based on the sidebar menu option
if page == "API Spec Validator":
    st.title("API Spec Validator")

    # File upload section
    uploaded_file = st.file_uploader("Upload your API Spec (JSON or YAML)", type=["json", "yaml"])
    if uploaded_file:
        # Load the file and perform validation
        try:
            if uploaded_file.name.endswith(".json"):
                api_spec = json.load(uploaded_file)
            else:
                api_spec = yaml.safe_load(uploaded_file)

            # Display validation results with user-friendly error messages
            st.subheader("Validation Results")
            validation_result, is_valid, error_list = validate_api_spec(api_spec)
            st.write(validation_result)

            # Display errors if validation fails
            if not is_valid:
                st.error("The following errors were found in the API specification:")
                for error in error_list:
                    st.write(f"- {error}")

            # If valid, generate and display documentation
            if is_valid:
                st.subheader("Generated Documentation")
                documentation = generate_documentation(api_spec)
                st.text_area("Documentation", documentation, height=300)

                # Option to download the documentation
                st.download_button(
                    label="Download Documentation",
                    data=documentation,
                    file_name="api_documentation.txt"
                )

        except Exception as e:
            st.error(f"Error processing the file: {str(e)}")

elif page == "API Guidance Chat":
    st.title("AI Guidance Chat")

    # Initialize Streamlit session state for AIbot chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

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
        st.write(f"You: {msg['user']}")
        st.write(f"AIbot: {msg['bot']}")
