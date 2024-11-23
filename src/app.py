import pandas         as pd
import streamlit      as st
import plotly.express as px


st.title("Vehicle Price Analysis")

uploaded_file = st.file_uploader("Choose file type", type=["csv"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, engine="openpyxlsx")

    st.write("### Know Data")
    st.dataframe(df)


