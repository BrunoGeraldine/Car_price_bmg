import pandas         as pd
import streamlit      as st
import plotly.express as px


from PIL import Image
from plotly import graph_objects as go

st.set_page_config(layout="wide")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# Carregar a imagem
image = Image.open('bmw.jpg')

# Criação das colunas para imagem e título
col1, col2 = st.columns([0.1, 0.9])  # Ajuste na largura das colunas
with col1:
    st.image(image, use_container_width=True)  # Ajuste para usar a largura da coluna

html_title = """
    <style>
    .title-test {
        font-weight: bold;
        padding: 10px; /* Aumentar padding para cima e baixo */
        margin: 0;
        border-radius: 6px;
        display: inline-block; /* Garantir que o elemento se comporte como bloco em linha */
    }
    </style>
    <center><h1 class="title-test">Vehicle Price Analysis</h1></center>"""
with col2:
    st.markdown(html_title, unsafe_allow_html=True)
    #The use_column_width parameter has been deprecated and will be removed in a future release. Please utilize the use_container_width parameter instead.

#st.title("Vehicle Price Analysis")


#st.write("### Know Data")
df = pd.read_csv('../dataset/df_final_model.csv', encoding='utf-8', sep=';')

df = df.drop('Unnamed: 0', axis=1)

df['model'] = df['model'].apply(lambda x: 'BMW ' + x)

df['price'] = df['price'].apply(lambda x: f"{x:.2f}")
df['price'] = df['price'].astype(float)

df['year'] = df['year'].astype(str)
df['year'] = df['year'].str.replace(',', '').astype(int)
#st.table(data=df.head())

#st.dataframe(df)

st.sidebar.header("Parameters")

# user input
#model_choosed = df['model']
model_choose = st.sidebar.selectbox('Choose the model', df['model'])

st.subheader('Model choose - ' + model_choose)
# 
#analise = st.sidebar.selectbox('Select type of analysis')
exec = st.sidebar.button('Excute')

if exec:

    #read dataframe
    st.dataframe(model_choose)


    st.write('### Average price for model')
    #avg_price_model = df.groupby('model')['price'].mean().reset_index()
    #avg_price_model_year = df.groupby(['model', 'year'])['price'].mean().reset_index()

    avg_price_model = df.groupby('model')['price'].mean().reset_index()
    avg_price_model_year = df.groupby(['model', 'year'])['price'].mean().reset_index()

    fig = px.bar(avg_price_model, x='model', y='price', title='Model Average Price')
    st.plotly_chart(fig)

    fig = px.bar(avg_price_model_year, x='model', y='year', title='Year Average Model Price')
    st.plotly_chart(fig)

else:
    st.dataframe(df)

