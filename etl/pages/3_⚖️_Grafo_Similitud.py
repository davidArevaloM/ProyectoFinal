import streamlit as st
import pandas as pd
import plotly.express as px
from neo4j import GraphDatabase
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.set_page_config(
    page_title="Similitud Providencias",
    page_icon="⚖️")

def consulta(providencia, similitud):
    # Consultar Información
    records, summary, keys = driver.execute_query(
        """MATCH (p1:Providencia {nombre: $nombre})-[r:Similar]->(p2:Providencia)
        WHERE r.similitud >= $similitud AND (p1.nombre = $nombre OR p2.nombre = $nombre)
        RETURN p1.nombre, p2.nombre, r.similitud""",
        nombre = providencia,
        similitud = similitud,
        database_="neo4j",
    )
    return pd.DataFrame(records)

# Conectar a la Base de Datos
URI = "neo4j+s://ce19c87f.databases.neo4j.io"
AUTH = ("neo4j", "GuPlCLhONEe3XnvgkzK6muCSK8WTRU8zZGt8kCzkb8A")

#Verifica Conexión con la base de datos
with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()

#Barra Lateral
with st.sidebar:
    providencia = st.text_input("Ingrese la providencia a consultar",
                               placeholder = "Ingrese la providencia a consultar")
    
    similitud = st.number_input("Insert el número de providencias a visualizar",
                               step = 0.01,
                               format = '%.2f',
                               value = 0.00)


# Crear el DataFrame
df = consulta(providencia, similitud)

#Titulo de la página
st.title('Providencias con Mayor Similitud')

if not df.empty:
    df.columns = ['Providencia1', 'Providencia2', 'Similitud']
    st.write(f'A continuación es posible observar el grafo de las {len(df)} providencias con mayor similitud a la providencia {providencia}. Al igual que el listado correspondiente ordenado de mayor a menor')
    # Crear un grafo vacío
    G = nx.Graph()

    # Agregar nodos y aristas desde el DataFrame
    for index, row in df.iterrows():
        origen = row['Providencia1']
        destino = row['Providencia2']
        similitud = row['Similitud']
        
        # Agregar arista si la similitud es mayor a un umbral
        if similitud > 0.5:
            G.add_edge(origen, destino, weight=similitud)

    # Obtener posiciones para cada nodo
    pos = nx.spring_layout(G)

    # Crear el gráfico de Plotly
    edge_x = []
    edge_y = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#24aba0'),
        hoverinfo='none',
        mode='lines')

    # Crear el gráfico de etiquetas de similitud
    edge_text_x = []
    edge_text_y = []
    edge_text = []
    for edge in G.edges(data=True):
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_text_x.append((x0 + x1) / 2)
        edge_text_y.append((y0 + y1) / 2)
        edge_text.append(f"{edge[2]['weight']:.2f}")

    edge_text_trace = go.Scatter(
        x=edge_text_x, y=edge_text_y,
        text=edge_text,
        mode='text',
        textposition="middle center",
        hoverinfo='none'
    )

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    #Dibujar los nodos
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        text=list(G.nodes),
        textposition="middle center",
        marker=dict(
            showscale=False,
            colorscale='haline',
            size=50,
            color = '#24aba0'
        ),
        textfont=dict(
            size=10,
            color="black" 
        )
    )

    #Crear Figura
    fig = go.Figure(data=[edge_trace, edge_text_trace, node_trace],
                    layout=go.Layout(
                        title='<br>Similitud entre Providencias',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

    #Ajustar tamaño
    fig.update_layout(
        width=800,
        height=800 
    )

    # Mostrar el gráfico
    st.plotly_chart(fig)

    st.markdown("#### Listado de providencias con mayor similitud.")
    # Mostrar el DataFrame
    st.dataframe(df.sort_values('Similitud', ascending=False), use_container_width=True)

else:
    st.markdown('## Ingrese la providencia que desea consultar junto con el valor de similitud de referencia')
