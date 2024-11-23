import pandas         as pd
import streamlit      as st
import plotly.express as px



st.title("Vehicle Price Analysis")


st.write("### Know Data")
df = pd.read_csv('../dataset/df_final_model.csv', encoding='utf-8', sep=';')

df = df.drop('Unnamed: 0', axis=1)

df['model'] = df['model'].apply(lambda x: 'BMW ' + x)
#st.table(data=df.head())

st.dataframe(df)

st.write('### Average price for model')
avg_price_model = df.groupby('model')['price'].mean().reset_index()

fig = px.bar(avg_price_model, x='model', y='price', title='Model Average Price')
st.plotly_chart(fig)
