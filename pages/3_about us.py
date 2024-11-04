import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="API Spec Validator"
)
# endregion <--------- Streamlit App Configuration --------->

st.markdown('''
# AI-Powered API Validation and Guidance Chat

## Problem Statement 
APIs play a crucial role in facilitating inter-agency communication and data exchange. However, they often encounter obstacles in three key areas:
- Interoperability
- Consistency
- Security

These challenges can result in:
- Complications during integration processes
- Inconsistent implementation of API practices
- Increased vulnerability to security risks

## Impact
Standardisation:
- Promote uniform API standards across the Whole-of-Government (WOG) ecosystem
- Enhance overall interoperability and consistency of APIs

Developer Efficiency:
- Streamline the validation process for API developers
- Allow developers to concentrate their efforts on API creation and enhancement, rather than manual compliance checks

## Proposed Solution
- Develop an AI-powered validation tool that automatically checks APIs for compliance with OpenAPI Standards
- Implement an intelligent recommendation engine that suggests improvements based on established API governance and best practices
- Create a conversational interface where users can query and receive instant guidance about OpenAPI Standards and requirements

## Data Sources
- [OpenAPI Standard](https://swagger.io/specification/)
- [API Standards and Governance](https://docs.developer.tech.gov.sg/docs/api-governance-model/pages/3-api-design)
''')
