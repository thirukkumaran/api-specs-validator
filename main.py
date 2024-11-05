import hmac
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


if not check_password():
    st.stop()  # Do not continue if check_password is not True.

with st.expander('Disclaimer'):
    st.write('''
**IMPORTANT NOTICE**: This web application is developed as a proof-of-concept prototype. The information provided here is **NOT intended for actual usage** and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

**Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.**

Always consult with qualified professionals for accurate and personalized advice.
''')

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
