import streamlit as st
import pymongo
from pymongo import MongoClient
import json
import pandas as pd

st.set_page_config(
    page_title="Consulta Providencias",
    page_icon="🔎",
)

connection_str = "mongodb+srv://ADMIN2:Vapu021292@cluster0.edkufrd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_str)
db = client["mlds3"]
collection = db["providencias"]

# Consultar una providencia por cualquier texto.
collection.create_index([("texto", "text")])

def query_texto(text):
    query = {"$text": {"$search": text}}
    projection = {"providencia": True,"tipo":True,"anio":True,"texto":True,"_id":False }
    return query, projection

# Consultar por el nombre de una providencia.
def query_providencia(providencia):
    query = {"providencia":providencia}
    projection = {"providencia": True,"tipo":True,"anio":True,"_id":False }
    return query, projection

# Consultar las sentencias por Tipo.
def query_tipo(tipo):
    query = {"tipo":tipo}
    projection = {"providencia": True,"tipo":True,"anio":True,"_id":False }
    return query, projection

# Consultar por un año especifico.
def query_anio(anio):
    query = {"anio":anio}
    projection = {"providencia": True,"tipo":True,"anio":True,"_id":False }
    return query, projection

#Mostrar datos
def print_result(data):
    df = pd.DataFrame(data)
        # Si el DataFrame no está vacío, mostrarlo como tabla
    if not df.empty:
        st.dataframe(df)
        #print(df.to_string(index=False))  # Imprime la tabla sin los índices de pandas
    else:
        st.warning("No se encontraron datos.")

st.markdown('# Consulta de Providencias')
st.write(""" En esta sección podra realizar busquedas sobre las providencias por medio de caracteristicas como el nombre, tipo, año o el contenido específico""")

resultados = None
with st.sidebar:
        provi = st.text_input("Ingrese el nombre de la providencia:")
        if st.button('Buscar por providencia'):
            resultados = list(collection.find(*query_providencia(provi)))

        tipo = st.text_input("Ingrese el tipo de sentencia:")
        if st.button('Buscar por tipo'):
            resultados = list(collection.find(*query_tipo(tipo)))

        anio = st.text_input("Ingrese el año de sentencia:")
        if st.button('Buscar por año'):
            resultados = list(collection.find(*query_anio(anio)))

        text = st.text_input("Ingrese el texto de sentencia:")
        if st.button('Buscar por texto'):
            resultados = list(collection.find(*query_texto(text)))

if resultados is not None:
    if len(resultados) != 0:
        st.markdown('<p style="font-size:20px; color:darkblue; font-style:italic; font-weight:bold;">Resultados de la Búsqueda:</p>', 
                    unsafe_allow_html=True)
        st.write(print_result(resultados))
    else:
        st.warning('No se encontraron resultados para la busqueda')