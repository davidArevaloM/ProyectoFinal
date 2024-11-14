import streamlit as st
from neo4j import GraphDatabase
import pandas as pd

st.set_page_config(
    page_title = 'Consultar Similitud',
    page_icon = '🧐'
)

st.markdown('# Consulta de Similitud')
st.write('En esta sección pordra realizar la consulta de la similitud de una providencia')

# Conectar a la Base de Datos
@st.cache_data(ttl=3600)
def consulta():
    URI = "neo4j+s://ce19c87f.databases.neo4j.io"
    AUTH = ("neo4j", "GuPlCLhONEe3XnvgkzK6muCSK8WTRU8zZGt8kCzkb8A")
    #Verifica Conexión con la base de datos
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()

    # Consultar Información
    records, summary, keys = driver.execute_query(
        """MATCH (p1:Providencia)-[Similar]->(p2:Providencia)
        RETURN p1.nombre as Prov_1, p2.nombre as Prov_2, Similar.similitud as Similitud
        ORDER BY Similitud DESC
        """,
        database_="neo4j",
    )
    return pd.DataFrame(records)

df = consulta()
df.columns = ['Providencia1', 'Providencia2', 'Similitud']

with st.sidebar:
    seleccion = st.text_input('Igrese la providencia que desea consultar',
                              placeholder = 'Igrese la providencia que desea consultar')

dff = df[df['Providencia1'] == seleccion].reset_index()

if not dff.empty:
    st.dataframe(dff[['Providencia1', 'Providencia2', 'Similitud']],
                 use_container_width=True)
    
    for i in range(len(dff)):
            sim = dff.loc[i, 'Similitud'].round(2)
            prov1 = dff.loc[i, 'Providencia1']
            prov2 = dff.loc[i, 'Providencia2']
            st.write(f"La providencia {prov1} posee un {sim} % de similitud con la providencia {prov2}")