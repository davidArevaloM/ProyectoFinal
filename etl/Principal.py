import streamlit as st

st.set_page_config(
    page_title="Lecciones Aprendidas",
    page_icon="🧠",
)

st.title('Lecciones Aprendidas')

st.markdown("""1. El uso de librerias como dask o Spark permiten optimizar la ejecución de los procesos debido a la paralelización de las tareas y rutinas de acuerdo con los recursos computacionales disponibles.\n
2. MongoDB Atlas permite la carga, escalabilidad y disponibilidad de grandes conjuntos de datos, realizando consultas de manera eficiente.\n
3. Neo4j permite el almacenamiento y representación de las relaciones entre los nodos a través de grafos, sin embargo, su disponibilidad se limita debido a la inactivación de la instancia. De igual forma, sus consultan tardan un poco más con respecto a MongoDB.\n
4. Streamlit permite la visualización de los resultados por medio de una codificación intuitiva y de baja complejidad.""")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.image("images/dask.jpeg", width=100)
with col2:
    st.image("images/Mongo2.jpeg", width=100)
with col3:
    st.image("images/eo4j.jpeg", width=100)
with col4:
    st.image("images/Streamlit.jpeg", width=100)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""*David Santiago Arévalo Monroy*\n
*Victor Alejandro Pinzón Ustate*\n
*Daniel Leonardo Montoya Gutierrez*""")