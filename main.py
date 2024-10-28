import json
import openai
import os
import streamlit as st
import yaml

from dotenv import load_dotenv
from typing import Any, Callable
from validator.api_standards_and_governance import validate_api_spec as validate_api_standards_and_governance
from validator.models import RequestModel, Report, ResponseModel
from validator.openapi_standard import validate_api_spec as validate_openapi_standard

# Load environment variables and set up OpenAI API key
load_dotenv('.env')
# openai.api_key = os.getenv('OPENAI_API_KEY')

os.environ['CURL_CA_BUNDLE'] = ''  # Ensure SSL handling if needed

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

def renderReportInMarkdown(report: Report):
    st.markdown(
        """
        <style>
        .normal {
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 10px;
            background-color: #f4f4f4;
            border: 1px solid #ddd;
        }
        .highlight {
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 10px;
            background-color: #e1f5fe;
            border: 1px solid #ddd;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(header(report.name, 1))
    for section in report.sections:
        st.markdown(header(section.id, 3) + ' ' + section.name)
        for rule in section.rules:
            if rule.humanReview:
                card(rule.rule, rule.recommendation, "normal")
            else:
                card(rule.rule, rule.recommendation, "highlight")

def header(s: str, n: int) -> str:
    return '#'*n + ' ' + s

def card(rule: str, recommendation: str, style: str) -> None:
    st.markdown(
        f'''
        <div class="{style}">
            <h4>{rule}</h4>
            {recommendation}
        </div>
        ''',
        unsafe_allow_html=True
    )
class Option:
    def __init__(self, name, validator: Callable[[Any], ResponseModel]):
        self.name = name
        self.validator = validator
        self.checked = False

# Display the selected page based on the sidebar menu option
if page == "API Spec Validator":
    st.title("API Spec Validator")

    options: list[Option] = []
    options.append(Option("OpenAPI Standard", validate_openapi_standard))
    options.append(Option("API Standard and Governance", validate_api_standards_and_governance))

    # File upload section
    uploaded_file = st.file_uploader("Upload your API Spec (JSON or YAML)", type=["json", "yaml"])
    if uploaded_file:
        # Load the file and perform validation
        try:
            if uploaded_file.name.endswith(".json"):
                req = RequestModel("json", json.load(uploaded_file))
            else:
                req = RequestModel("yaml", yaml.safe_load(uploaded_file))

            st.subheader("Generate report for the following:")

            tabNames: list[str] = []
            for i in range(len(options)):
                options[i].checked = st.checkbox(options[i].name, True)
                if options[i].checked:
                    tabNames.append(options[i].name)

            if 0 < len(tabNames):
                t = st.tabs(tabNames)
                ci = 0
                for i in range(len(options)):
                    if options[i].checked:
                        with t[ci]:
                            with st.spinner('Generating report...'):
                                response = options[ci].validator(req)
                            renderReportInMarkdown(response.report)
                        ci += 1

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
