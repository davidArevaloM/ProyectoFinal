import streamlit as st
from neo4j import GraphDatabase
import pandas as pd

st.set_page_config(
    page_title = 'Consultar Similitud',
    page_icon = '🧐'
)

st.markdown('# Consulta de Similitud')
st.write('En esta sección podra realizar la consulta de la similitud de una providencia')

def consulta(providencia):
    # Consultar Información
    records, summary, keys = driver.execute_query(
        """MATCH (p1:Providencia {nombre: $nombre})-[r:Similar]->(p2:Providencia)
        RETURN p1.nombre, p2.nombre, r.similitud""",
        nombre=providencia,
        database_="neo4j",
    )
    return pd.DataFrame(records)

# Conectar a la Base de Datos
URI = "neo4j+s://ce19c87f.databases.neo4j.io"
AUTH = ("neo4j", "GuPlCLhONEe3XnvgkzK6muCSK8WTRU8zZGt8kCzkb8A")

#Verifica Conexión con la base de datos
with GraphDatabase.driver(URI, auth=AUTH) as driver:
     driver.verify_connectivity()

with st.sidebar:
    seleccion = st.text_input('Ingrese la providencia que desea consultar',
                              placeholder = 'Ingrese la providencia que desea consultar')

dff = consulta(seleccion)

if not seleccion == '':
    if not dff.empty:
        dff.columns = ['Providencia1', 'Providencia2', 'Similitud']
        st.markdown('<p style="font-size:20px; color:darkblue; font-style:italic; font-weight:bold;">Resultados de la Búsqueda:</p>', 
                    unsafe_allow_html=True)
        st.dataframe(dff[['Providencia1', 'Providencia2', 'Similitud']],
                     use_container_width=True)
            
        for i in range(len(dff)):
                sim = dff.loc[i, 'Similitud'].round(2)
                prov1 = dff.loc[i, 'Providencia1']
                prov2 = dff.loc[i, 'Providencia2']
                st.write(f"La providencia {prov1} posee un {sim} % de similitud con la providencia {prov2}")
    else:
        st.warning("No se encontraron resultados para la consulta.")