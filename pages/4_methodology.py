import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Methodology",
)
# endregion <--------- Streamlit App Configuration --------->

st.markdown('''
# Methodology
''')

st.markdown('''
## OpenAPI Standard
''')

st.image('./pages/4_methodology_openapi_standard.png')
# graph TD
#     A[Start] --> B[Upload API Spec File]
#     B --> C[Read Latest OpenAPI Spec from Disc]
#     C --> D[Process Uploaded API Spec]
#     D --> E{<b>Determine File Type</b>}
#     E -->|JSON| F[Identify as JSON]
#     E -->|YAML| G[Identify as YAML]
#     F --> H[<b>Check Version Compatibility</b>]
#     G --> H
#     H --> I[<b>Generate Validation Results</b>]
#     I --> J[Output Results]
#     J --> K[End]
#
#     subgraph "Output"
#     J --> L[<font color="green">File Type: JSON/YAML</font>]
#     J --> M[<font color="green">Version Compatibility</font>]
#     J --> N[<font color="green">Success or List of Errors</font>]
#     end

st.markdown('''
## API Standards and Governance
''')

st.image('./pages/4_methodology_api_standards_and_governance.png')

# graph TD
#     A[Start] --> B[Upload API Spec File]
#     B --> C[Read API Standards and Governance Rules]
#     C --> D{Process Rules in Parallel}
#
#     D --> |Rule 1| E1{Requires Human Review?}
#     D --> |Rule 2| E2{Requires Human Review?}
#     D --> |Rule 3| E3{Requires Human Review?}
#     D --> |...| E4[...]
#
#     E1 -->|Yes| F1[Indicate Limitation]
#     E1 -->|No| G1[Create Prompt for LLM]
#     G1 --> H1[LLM Provides Recommendations]
#
#     E2 -->|Yes| F2[Indicate Limitation]
#     E2 -->|No| G2[Create Prompt for LLM]
#     G2 --> H2[LLM Provides Recommendations]
#
#     E3 -->|Yes| F3[Indicate Limitation]
#     E3 -->|No| G3[Create Prompt for LLM]
#     G3 --> H3[LLM Provides Recommendations]
#
#     F1 --> I[Collect Results]
#     F2 --> I
#     F3 --> I
#     H1 --> I
#     H2 --> I
#     H3 --> I
#     E4 --> I

#     I --> J[Output Final Recommendations and Limitations]
#     J --> K[End]

st.markdown('''
## Guidance Chat
''')

st.image('./pages/4_methodology_guidance_chat.png')

# graph TD
#     A[Start] --> B[Initialize FAISS Index with API Standards and Governance Documents]
#     B --> C[Accept User Query]
#     C --> D[Send Query to LLM]
#     D --> E[Get Response from LLM]
#     E --> F[Display Response to User]
#     F --> G{Wait for Next Query}
#     G -->|New Query| C
#     G -->|No Query| H[End]
#
#     style A fill:#f9f,stroke:#333,stroke-width:2px
#     style H fill:#f9f,stroke:#333,stroke-width:2px
#     style G fill:#bbf,stroke:#333,stroke-width:2px
#     style B fill:#ffa,stroke:#333,stroke-width:2px


