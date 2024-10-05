import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="API Spec Validator"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About this App")

st.write("API Spec Validator")

with st.expander("How to use this App"):
    st.write("1. Upload your API Spec.")

